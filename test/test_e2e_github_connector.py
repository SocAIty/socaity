"""E2E Phase 8: GitHub connector through catalog, workflow, job.

Register the canonical GitHub OpenAPI document, register it again (the platform
answers ``connector_exists`` with the same service), pin the connector as a
``ServiceNode`` searching ``socaity_frontend``, run the workflow and check the
private repository shows up. The child job is a normal catalog job on the
external details binding and carries the job-floor charge.

    python test/test_e2e_github_connector.py
    pytest test/test_e2e_github_connector.py -v -s

Keys: see ``agentic_utils``.
"""
from __future__ import annotations

import sys
import time
from pathlib import Path
from uuid import uuid4

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import agentic_utils as env  # noqa: E402  (sets URL defaults before socaity import)

from socaity import Session, client  # noqa: E402
from socaity_cli.errors import BackendApiError  # noqa: E402

GITHUB_SPEC_URL = (
    "https://raw.githubusercontent.com/github/rest-api-description/main/"
    "descriptions/api.github.com/api.github.com.json"
)
PRIVATE_REPO = "socaity_frontend"

pytestmark = [
    pytest.mark.skipif(not env.backend_up(), reason=f"backend not reachable at {env.BACKEND}"),
    pytest.mark.skipif(not env.inference_up(), reason=f"APIPod gate not reachable at {env.GATE}"),
    pytest.mark.skipif(not env.api_key(), reason=env.missing_env("SOCAITY_API_KEY") or "no SOCAITY_API_KEY"),
]


def _register(source: str) -> tuple[str, bool]:
    """Return ``(service_id, already_existed)`` for one register call."""
    try:
        service = client.register_connector(source)
    except BackendApiError as exc:
        assert exc.status_code == 409 and exc.code == "connector_exists", (exc.status_code, exc.code, str(exc))
        return exc.detail["service"]["id"], True
    assert service is not None, f"register rejected {source}"
    return service.id, False


def _connector_doc(service, endpoint) -> dict:
    details = service.details[0]
    return {
        "id": f"wf_{uuid4()}",
        "title": "GitHub connector e2e",
        "goal": f"Find the private {PRIVATE_REPO} repository through the GitHub connector.",
        "nodes": [
            {"id": "nd_input", "kind": "builtin", "title": "input"},
            {
                "id": "nd_gh",
                "kind": "service",
                "title": "github search repos",
                "service_id": service.id,
                "endpoint_id": endpoint.id,
                "details_id": details.id,
                "connectors_id": details.connector.id,
                "path": endpoint.path,
                "specification_hash": details.specification_hash,
                "inputs": {"q": PRIVATE_REPO},
            },
            {"id": "nd_output", "kind": "builtin", "title": "output"},
        ],
        "edges": [
            {"id": "ed_in_gh", "source": "nd_input", "target": "nd_gh"},
            {"id": "ed_gh_out", "source": "nd_gh", "target": "nd_output"},
        ],
    }


def _child_job(wf_id: str, parent_job_id: str, details_id: str):
    for row in client.query_workflow_runs(wf_id):
        live = client.get_workflow_run(row.id, expand=["traces"]) or row
        for trace in live.traces or []:
            job_id = getattr(trace, "job_id", None)
            if job_id and job_id != parent_job_id:
                job = client.get_job(job_id)
                if job and job.details_id == details_id:
                    return job
    return None


def run() -> None:
    session = Session(api_key=env.api_key(), backend_url=env.BACKEND)
    with session:
        env.log("T8.1", f"register {GITHUB_SPEC_URL}")
        service_id, existed = _register(GITHUB_SPEC_URL)
        env.log("T8.1", f"service_id={service_id} already_existed={existed}")

        again_id, again_existed = _register(GITHUB_SPEC_URL)
        env.log("T8.1", f"second register service_id={again_id} already_existed={again_existed}")
        assert again_existed, "second register of the same OpenAPI document created a new connector"
        assert again_id == service_id, (again_id, service_id)

        hits = client.query_services(q="github", filters=["kind:eq:connector"], limit=50, mine=True)
        env.log("T8.2", f"catalog hits={[row.slug for row in hits]}")
        assert service_id in {row.id for row in hits}, "connector missing from catalog search"

        service = client.get_service(
            service_id,
            expand=["details.contract", "details.connector", "endpoints", "credential_requirements"],
        )
        assert service is not None and service.kind == "connector", service
        details = service.details[0]
        assert details.execution == "external", details.execution
        assert details.deployment is None, "connector must not have a hosting row"
        assert details.connector and details.connector.id, "connector row missing"
        assert details.spec_url == GITHUB_SPEC_URL, details.spec_url
        endpoint = next((row for row in service.endpoints if row.path == "/search/repositories"), None)
        assert endpoint is not None, "GET /search/repositories missing from connector endpoints"
        env.log(
            "T8.2",
            f"details_id={details.id} connectors_id={details.connector.id} "
            f"credentials={sorted(row.name for row in service.credential_requirements or [])}",
        )

        saved = client.upsert_workflow(
            _connector_doc(service, endpoint), slug=f"wf-github-e2e-{int(time.time())}", message="github e2e",
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
        search = outputs.get("nd_gh") or outputs.get("nd_output") or {}
        names = [item.get("name") for item in (search.get("items") or []) if isinstance(item, dict)]
        env.log("T8.3", f"total_count={search.get('total_count')} names={names[:10]}")
        assert PRIVATE_REPO in names, f"private repository {PRIVATE_REPO} not in search results: {names[:10]}"

        child = _child_job(wf_id, finished.get("job_id"), details.id)
        assert child is not None, "connector child job was not recorded on the workflow run"
        billed = client.get_job(child.id, expand=["billing"])
        env.log("T8.4", f"child job={child.id} status={billed.status} billing={billed.billing}")
        assert (billed.status or "").lower() in ("finished", "completed", "success"), billed.status
        assert billed.billing is not None, "job-floor billing missing on connector job"
        assert billed.billing.cost_amount is not None and billed.billing.cost_amount >= 0, billed.billing
    env.log("T8", "PASS")


def test_github_connector_catalog_workflow_job() -> None:
    run()


if __name__ == "__main__":
    run()
