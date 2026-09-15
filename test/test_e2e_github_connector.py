"""E2E Phase 8: official GitHub connector through catalog, workflow, job.

Connect via ``socaity connect github``, find the row, pin it as a
``ServiceNode``, run the workflow. Credential names are stored; the child
job is a normal catalog job on the external details binding. Vault inject
is Phase 9; this path uses a public GitHub read so no token is required.

    python test/test_e2e_github_connector.py
    pytest test/test_e2e_github_connector.py -v -s

Keys: see ``agentic_utils``.
"""
from __future__ import annotations

import io
import sys
import time
from pathlib import Path
from uuid import uuid4

import httpx
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import agentic_utils as env  # noqa: E402  (sets URL defaults before socaity import)

import socaity  # noqa: E402
from socaity import Session, client  # noqa: E402
from socaity_cli.cli import main as cli_main  # noqa: E402

SLUG = f"github-e2e-{int(time.time())}"
SEARCH_Q = "socaity"

pytestmark = [
    pytest.mark.skipif(not env.backend_up(), reason=f"backend not reachable at {env.BACKEND}"),
    pytest.mark.skipif(not env.inference_up(), reason=f"APIPod gate not reachable at {env.GATE}"),
    pytest.mark.skipif(not env.api_key(), reason=env.missing_env("SOCAITY_API_KEY") or "no SOCAITY_API_KEY"),
]


def _wait_gate_route(details_id: str, path: str, timeout_s: float = 45) -> None:
    """First 404 remounts the binding; later statuses mean the route is live."""
    url = f"{env.GATE}/services/v1/{details_id}{path}"
    deadline = time.monotonic() + timeout_s
    last = None
    while time.monotonic() < deadline:
        try:
            last = httpx.post(url, json={}, timeout=10)
            if last.status_code != 404:
                return
        except httpx.HTTPError as exc:
            last = exc
        time.sleep(1)
    raise AssertionError(f"gate did not mount {url} within {timeout_s}s (last={last})")


def _run_cli(*argv: str) -> str:
    buffer = io.StringIO()
    stdout, sys.stdout = sys.stdout, buffer
    try:
        cli_main(list(argv))
    finally:
        sys.stdout = stdout
    return buffer.getvalue()


def _connector_doc(service) -> dict:
    details = service.details[0]
    endpoint = next(row for row in service.endpoints if row.path == "/search/repositories")
    return {
        "id": f"wf_{uuid4()}",
        "title": f"GitHub connector {SLUG}",
        "goal": "Search public repositories through the GitHub connector.",
        "nodes": [
            {"id": "nd_input", "kind": "builtin", "title": "input"},
            {
                "id": "nd_gh",
                "kind": "service",
                "title": "github search repos",
                "service_id": service.id,
                "endpoint_id": endpoint.id,
                "details_id": details.id,
                "path": endpoint.path,
                "specification_hash": details.specification_hash,
                "inputs": {"q": SEARCH_Q},
            },
            {"id": "nd_output", "kind": "builtin", "title": "output"},
        ],
        "edges": [
            {"id": "ed_in_gh", "source": "nd_input", "target": "nd_gh"},
            {"id": "ed_gh_out", "source": "nd_gh", "target": "nd_output"},
        ],
    }


def run() -> None:
    session = Session(api_key=env.api_key(), backend_url=env.BACKEND)
    with session:
        env.log("T8.1", f"socaity connect github --slug {SLUG}")
        output = _run_cli("connect", "github", "--slug", SLUG)
        env.log("T8.1", output.strip() or "(no cli stdout)")
        assert "Connected" in output, output
        assert SLUG in output, output
        assert "GitHubAuth" in output, output

        hits = client.query_services(q=SLUG, filters=["kind:eq:connector"], limit=10)
        slugs = [row.slug for row in hits]
        env.log("T8.2", f"catalog hits={slugs}")
        assert any(row.slug == SLUG for row in hits), slugs

        service = client.get_service(SLUG, expand=["details.contract", "endpoints", "credential_requirements"])
        assert service is not None, f"get_service missed {SLUG}"
        assert service.kind == "connector", service.kind
        assert service.details, "connector has no details binding"
        details = service.details[0]
        assert details.execution == "external", details.execution
        assert details.deployment is None, "connector must not have a hosting row"
        names = {row.name for row in (service.credential_requirements or [])}
        env.log("T8.2", f"details_id={details.id} credentials={sorted(names)}")
        assert "GitHubAuth" in names, names
        paths = {row.path for row in service.endpoints}
        assert "/search/repositories" in paths, paths
        env.log("T8.2", "waiting for gate to mount the connector")
        _wait_gate_route(details.id, "/search/repositories")

        saved = client.upsert_workflow(
            _connector_doc(service),
            slug=f"wf-{SLUG}",
            message="github connector e2e",
        )
        assert saved and saved.workflow, "workflow upsert failed"
        wf_id = saved.workflow.id
        env.log("T8.3", f"workflow id={wf_id}")

        finished = env.run_workflow(wf_id, inputs={}, timeout_s=300)
        env.log("T8.3", f"run job={finished.get('job_id')} status={finished.get('status')} error={finished.get('error')}")
        assert finished.get("status") == "finished", finished
        result = finished.get("result") or {}
        assert result.get("status") == "completed", result

        outputs = result.get("outputs") or {}
        repo_out = outputs.get("nd_gh") or outputs.get("nd_output") or result
        blob = str(repo_out).lower()
        env.log("T8.3", f"output={str(repo_out)[:400]}")
        assert SEARCH_Q in blob or "total_count" in blob or "items" in blob or "git" in blob, repo_out

        child = None
        runs = client.query_workflow_runs(wf_id)
        for row in runs:
            live = client.get_workflow_run(row.id, expand=["traces"]) or row
            for trace in live.traces or []:
                job_id = getattr(trace, "job_id", None)
                if job_id and job_id != finished.get("job_id"):
                    child = client.get_job(job_id)
                    if child:
                        break
            if child:
                break
        if child is None:
            jobs = client.query_jobs(filters=[f"details_id:eq:{details.id}"], expand=["billing"], limit=10)
            done = ("finished", "completed", "success")
            child = next(
                (job for job in jobs if (job.status or "").lower() in done),
                next((job for job in jobs if job.details_id == details.id), None),
            )
        assert child is not None, "connector child job was not enqueued"
        env.log("T8.4", f"child job={child.id} status={child.status} details_id={child.details_id}")
        assert child.details_id == details.id, (child.details_id, details.id)

        deadline = time.monotonic() + 60
        billed = None
        while time.monotonic() < deadline:
            billed = client.get_job(child.id, expand=["billing"])
            status = ((billed.status if billed else child.status) or "").lower()
            if status in ("finished", "completed", "success"):
                break
            time.sleep(2)
        else:
            raise AssertionError(f"connector child job {child.id} did not finish (last={billed or child})")
        billing = billed.billing if billed else None
        env.log("T8.4", f"status={billed.status if billed else None} billing={billing}")
        assert billing is not None, "job-floor billing missing on connector job"
        cost = getattr(billing, "cost_amount", None)
        if cost is None:
            cost = getattr(billing, "customer_charge_amount", None)
        assert cost is not None, billing
        assert cost >= 0, cost
    env.log("T8", "PASS")


def test_github_connector_catalog_workflow_job() -> None:
    run()


if __name__ == "__main__":
    run()
