"""E2E Phase 9: GitHub MCP credential lifecycle.

Inspect without a credential answers ``auth_required`` and advertises both a token
(``secret``) and OAuth. Connect with ``GITHUB_TOKEN``, call ``list_branches`` on the
private ``socaity_frontend`` repository, disconnect (the same call now fails), then
change the credential to OAuth. OAuth waits for a human login in the browser, so
that step is a manual gate: it runs with ``SOCAITY_E2E_MANUAL=1`` only. Without it
the token binding is restored so the connector stays usable.

    python test/test_e2e_github_mcp.py
    SOCAITY_E2E_MANUAL=1 pytest test/test_e2e_github_mcp.py -v -s

Keys: see ``agentic_utils``.
"""
from __future__ import annotations

import os
import sys
import webbrowser
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import agentic_utils as env  # noqa: E402  (sets URL defaults before socaity import)

from socaity import Session, client  # noqa: E402
from socaity_cli.errors import BackendApiError  # noqa: E402
from test_e2e_github_connector import (  # noqa: E402
    GITHUB_MCP_URL,
    PRIVATE_REPO,
    REPO_OWNER,
    connect_github_mcp,
    lists_branches,
    tool_endpoint,
)

MANUAL = os.getenv("SOCAITY_E2E_MANUAL") == "1"

pytestmark = [
    pytest.mark.skipif(not env.backend_up(), reason=f"backend not reachable at {env.BACKEND}"),
    pytest.mark.skipif(not env.inference_up(), reason=f"APIPod gate not reachable at {env.GATE}"),
    pytest.mark.skipif(not env.api_key(), reason=env.missing_env("SOCAITY_API_KEY") or "no SOCAITY_API_KEY"),
    pytest.mark.skipif(not os.getenv("GITHUB_TOKEN"), reason=env.missing_env("GITHUB_TOKEN") or "no GITHUB_TOKEN"),
]


def _list_branches(target: str) -> str:
    job = client.run(target, params={"arguments": {"owner": REPO_OWNER, "repo": PRIVATE_REPO}})
    return str(job.get_result(timeout_s=180))


def _open_authorize(event: str, data: dict) -> None:
    if event == "authorize":
        env.log("T9.4", f"authorize at {data.get('url')}")
        webbrowser.open(data["url"])


def run() -> None:
    with Session(api_key=env.api_key(), backend_url=env.BACKEND):
        with pytest.raises(BackendApiError) as protected:
            client.inspect_connector(GITHUB_MCP_URL)
        detail = protected.value.detail or {}
        env.log("T9.1", f"code={protected.value.code} alternatives={detail.get('alternatives')}")
        assert protected.value.status_code == 422 and protected.value.code == "auth_required", str(protected.value)
        assert {"secret", "oauth"} <= set(detail.get("alternatives") or []), detail
        assert detail.get("authorization_servers"), "no OAuth authorization server advertised"

        service_id, existed = connect_github_mcp()
        service = client.get_service(service_id, expand=["details.contract", "endpoints"])
        target = f"{service.slug}/{tool_endpoint(service, 'list_branches').operation_key}"
        env.log("T9.2", f"service_id={service_id} already_existed={existed} target={target}")
        branches = _list_branches(target)
        env.log("T9.2", f"token call={branches[:200]}")
        assert lists_branches(branches), branches[:300]

        client.disconnect_connector_credential(service_id)
        with pytest.raises(Exception) as unauthorized:
            _list_branches(target)
        env.log("T9.3", f"after disconnect: {unauthorized.value}")

        if not MANUAL:
            client.change_connector_credential(service_id, secret=os.environ["GITHUB_TOKEN"])
            env.log("T9.4", "OAuth is a manual gate; set SOCAITY_E2E_MANUAL=1. Token binding restored.")
            return
        binding = client.change_connector_credential(service_id, oauth=True, on_event=_open_authorize)
        env.log("T9.4", f"oauth binding={binding}")
        branches = _list_branches(target)
        assert lists_branches(branches), branches[:300]
    env.log("T9", "PASS")


def test_github_mcp_credential_lifecycle() -> None:
    run()


if __name__ == "__main__":
    run()
