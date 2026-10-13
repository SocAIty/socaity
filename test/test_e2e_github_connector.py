"""E2E Phase 8: GitHub connector through catalog, workflow, job.

The full GitHub REST description (about 1200 operations) exceeds the 500-operation
inspect cap: register rejects it before anything persists. GitHub publishes no
smaller official REST description, so the private-repository call runs through the
official GitHub MCP server. Register it with ``GITHUB_TOKEN`` (a second register
answers ``connector_exists`` with the same service), pin ``list_branches`` on the
private ``socaity_frontend`` repository as a ``ServiceNode``, run the workflow and
check the child job carries the job-floor charge.

    python test/test_e2e_github_connector.py
    pytest test/test_e2e_github_connector.py -v -s

Keys: see ``agentic_utils``.
"""
from __future__ import annotations

import os
import sys
import time
from pathlib import Path
from uuid import uuid4

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import agentic_utils as env  # noqa: E402  (sets URL defaults before socaity import)

from apipod_registry import active_details  # noqa: E402
from socaity import Session, client  # noqa: E402
from socaity_cli.errors import BackendApiError  # noqa: E402

GITHUB_SPEC_URL = (
    "https://raw.githubusercontent.com/github/rest-api-description/main/"
    "descriptions/api.github.com/api.github.com.json"
)
GITHUB_MCP_URL = "https://api.githubcopilot.com/mcp/"
REPO_OWNER = "w4hns1nn"
PRIVATE_REPO = "socaity_frontend"
INSPECT_LIMIT_CODES = {"too_many_operations", "document_too_large"}

pytestmark = [
    pytest.mark.skipif(not env.backend_up(), reason=f"backend not reachable at {env.BACKEND}"),
    pytest.mark.skipif(not env.inference_up(), reason=f"APIPod gate not reachable at {env.GATE}"),
    pytest.mark.skipif(not env.api_key(), reason=env.missing_env("SOCAITY_API_KEY") or "no SOCAITY_API_KEY"),
    pytest.mark.skipif(not os.getenv("GITHUB_TOKEN"), reason=env.missing_env("GITHUB_TOKEN") or "no GITHUB_TOKEN"),
]


def connect_github_mcp() -> tuple[str, bool]:
    """Return ``(service_id, already_existed)``; an existing connector gets ``GITHUB_TOKEN`` bound again."""
    token = os.environ["GITHUB_TOKEN"]
    try:
        return client.register_connector(GITHUB_MCP_URL, secret=token).id, False
    except BackendApiError as exc:
        assert exc.status_code == 409 and exc.code == "connector_exists", (exc.status_code, exc.code, str(exc))
        service_id = exc.detail["service"]["id"]
    client.change_connector_credential(service_id, secret=token)
    return service_id, True


def lists_branches(output) -> bool:
    """MCP ``structuredContent`` arrives as branch objects (Python repr once stringified), text as JSON."""
    text = str(output)
    return "'name': " in text or '"name": ' in text


def tool_endpoint(service, tool: str):
    """Catalog endpoint of one MCP tool; the provider tool name stays in the contract's ``operation_id``."""
    contract_endpoints = active_details(service).contract.endpoints
    key = next((row.operation_key for row in contract_endpoints if row.operation_id == tool), None)
    endpoint = next((row for row in service.endpoints or [] if row.operation_key == key), None)
    assert endpoint is not None, f"tool {tool} missing from {sorted(row.operation_id for row in contract_endpoints)}"
    return endpoint


def _connector_doc(service, endpoint) -> dict:
    details = active_details(service)
    assert details is not None and details.connector is not None
    return {
        "id": f"wf_{uuid4()}",
        "title": "GitHub connector e2e",
        "goal": f"List the branches of the private {PRIVATE_REPO} repository through the GitHub MCP connector.",
        "nodes": [
            {"id": "nd_input", "kind": "builtin", "title": "input"},
            {
                "id": "nd_gh",
                "kind": "service",
                "title": "github list branches",
                "service_id": service.id,
                "endpoint_id": endpoint.id,
                "details_id": details.id,
                "connectors_id": details.connector.id,
                "operation_key": endpoint.operation_key,
                "specification_hash": details.specification_hash,
                "inputs": {"arguments": {"owner": REPO_OWNER, "repo": PRIVATE_REPO}},
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
        for attempt in ("first", "second"):
            env.log("T8.1", f"{attempt} register of the full REST description {GITHUB_SPEC_URL}")
            with pytest.raises(BackendApiError) as rejected:
                client.register_connector(GITHUB_SPEC_URL)
            env.log("T8.1", f"status={rejected.value.status_code} code={rejected.value.code}")
            # A second identical rejection (not connector_exists) proves nothing persisted.
            assert rejected.value.code in INSPECT_LIMIT_CODES, (rejected.value.code, str(rejected.value))

        service_id, existed = connect_github_mcp()
        env.log("T8.2", f"github mcp service_id={service_id} already_existed={existed}")
        with pytest.raises(BackendApiError) as again:
            client.register_connector(GITHUB_MCP_URL, secret=os.environ["GITHUB_TOKEN"])
        assert again.value.code == "connector_exists", (again.value.code, str(again.value))
        assert again.value.detail["service"]["id"] == service_id, again.value.detail["service"]["id"]

        hits = client.query_services(q="github", filters=["kind:eq:connector"], limit=50, mine=True)
        env.log("T8.2", f"catalog hits={[row.slug for row in hits]}")
        assert service_id in {row.id for row in hits}, "connector missing from catalog search"

        service = client.get_service(
            service_id,
            expand=["details.contract", "details.connector", "endpoints", "credential_requirements"],
        )
        assert service is not None and service.kind == "connector", service
        details = active_details(service)
        assert details is not None, "connector has no active details binding"
        assert details.execution == "external", details.execution
        assert details.deployment is None, "connector must not have a hosting row"
        assert details.connector and details.connector.id, "connector row missing"
        assert details.contract.specification == "mcp", details.contract.specification
        endpoint = tool_endpoint(service, "list_branches")
        env.log("T8.2", f"details_id={details.id} tools={len(service.endpoints)} key={endpoint.operation_key}")

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
        branches = str(outputs.get("nd_gh") or outputs.get("nd_output") or "")
        env.log("T8.3", f"list_branches output={branches[:300]}")
        assert lists_branches(branches), f"no branch listed for private {REPO_OWNER}/{PRIVATE_REPO}: {branches[:300]}"

        child = _child_job(wf_id, finished.get("job_id"), details.id)
        assert child is not None, "connector child job was not recorded on the workflow run"
        billed = client.get_job(child.id, expand=["billing"])
        env.log("T8.4", f"child job={child.id} status={billed.status} billing={billed.billing}")
        assert (billed.status or "").lower() in ("finished", "completed", "success"), billed.status
        assert billed.billing is not None, "job-floor billing missing on connector job"
        assert billed.billing.cost_amount is not None and billed.billing.cost_amount > 0, billed.billing
    env.log("T8", "PASS")


def test_github_connector_catalog_workflow_job() -> None:
    run()


if __name__ == "__main__":
    run()
