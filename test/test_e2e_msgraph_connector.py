"""E2E Phase 10: Microsoft Graph OpenAPI against the inspect limits.

The full v1.0 description is rejected before anything persists (15 MB or 500
operations). The Mail subgraph Microsoft publishes for its PowerShell SDK fits
under the cap and registers as a connector with every inspected operation.

    python test/test_e2e_msgraph_connector.py
    pytest test/test_e2e_msgraph_connector.py -v -s

Keys: see ``agentic_utils``.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import agentic_utils as env  # noqa: E402  (sets URL defaults before socaity import)

from socaity import Session, client  # noqa: E402
from socaity_cli.errors import BackendApiError  # noqa: E402

GRAPH_FULL_URL = "https://raw.githubusercontent.com/microsoftgraph/msgraph-metadata/master/openapi/v1.0/openapi.yaml"
GRAPH_MAIL_URL = "https://raw.githubusercontent.com/microsoftgraph/msgraph-sdk-powershell/main/openApiDocs/v1.0/Mail.yml"
INSPECT_LIMIT_CODES = {"too_many_operations", "document_too_large"}
MAX_OPERATIONS = 500

pytestmark = [
    pytest.mark.skipif(not env.backend_up(), reason=f"backend not reachable at {env.BACKEND}"),
    pytest.mark.skipif(not env.api_key(), reason=env.missing_env("SOCAITY_API_KEY") or "no SOCAITY_API_KEY"),
]


def run() -> None:
    with Session(api_key=env.api_key(), backend_url=env.BACKEND):
        env.log("T10.1", f"inspect full Graph v1.0 {GRAPH_FULL_URL}")
        with pytest.raises(BackendApiError) as rejected:
            client.inspect_connector(GRAPH_FULL_URL)
        env.log("T10.1", f"status={rejected.value.status_code} code={rejected.value.code}")
        assert rejected.value.code in INSPECT_LIMIT_CODES, (rejected.value.code, str(rejected.value))

        try:
            preview = client.inspect_connector(GRAPH_MAIL_URL)
        except BackendApiError as exc:
            # A previous run registered the subgraph; inspect then answers 409 with that connector.
            assert exc.code == "connector_exists", (exc.code, str(exc))
            service = client.get_service(exc.detail["service"]["id"], expand=["endpoints"])
            env.log("T10.2", f"already registered service_id={service.id} endpoints={len(service.endpoints or [])}")
            assert service.kind == "connector", service.kind
            assert 0 < len(service.endpoints or []) <= MAX_OPERATIONS, len(service.endpoints or [])
            env.log("T10", "PASS")
            return
        operations = preview["operations"]
        env.log("T10.2", f"mail subgraph spec={preview['specification']} operations={len(operations)}")
        assert preview["specification"] == "openapi", preview["specification"]
        assert 0 < len(operations) <= MAX_OPERATIONS, len(operations)

        service = client.get_service(client.register_connector(GRAPH_MAIL_URL).id, expand=["endpoints"])
        env.log("T10.2", f"service_id={service.id} slug={service.slug} endpoints={len(service.endpoints or [])}")
        assert service.kind == "connector", service.kind
        assert {row.operation_key for row in service.endpoints} == {row["operation_key"] for row in operations}
    env.log("T10", "PASS")


def test_msgraph_connector_limits() -> None:
    run()


if __name__ == "__main__":
    run()
