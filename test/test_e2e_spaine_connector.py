"""E2E acceptance 5: SPAINE connects the GitHub MCP from a bare prompt.

The agent gets only ``connect the github MCP and add it to the workflow``: no URL, no draft.
It is expected to find the endpoint with ``web_search`` (a ``tavily/tavily-search`` job),
register it with ``add_connector`` and put one of its tools into the workflow it builds.

    python test/test_e2e_spaine_connector.py
    pytest test/test_e2e_spaine_connector.py -v -s

Keys: see ``agentic_utils``.
"""
from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import agentic_utils as env  # noqa: E402  (sets URL defaults before socaity import)

from apipod_registry import active_details  # noqa: E402
from socaity import Session, client  # noqa: E402

AGENT = "spaine"
PROMPT = "connect the github MCP and add it to the workflow"
TAVILY = "tavily"
GITHUB_MCP_HOST = "api.githubcopilot.com"

pytestmark = [
    pytest.mark.skipif(not env.backend_up(), reason=f"backend not reachable at {env.BACKEND}"),
    pytest.mark.skipif(not env.inference_up(), reason=f"APIPod gate not reachable at {env.GATE}"),
    pytest.mark.skipif(not env.api_key(), reason=env.missing_env("SOCAITY_API_KEY") or "no SOCAITY_API_KEY"),
]


def _searched_since(started_at: datetime, tavily_id: str) -> list:
    return [
        job for job in client.query_jobs(limit=50)
        if job.service_id == tavily_id and job.created_at
        and datetime.fromisoformat(job.created_at.replace("Z", "+00:00")) >= started_at
    ]


def _is_github_mcp(service_id: str) -> bool:
    service = client.get_service(service_id, expand=["details.connector"])
    details = active_details(service) if service else None
    return bool(details and GITHUB_MCP_HOST in (details.spec_url or ""))


def run() -> None:
    with Session(api_key=env.api_key(), backend_url=env.BACKEND):
        tavily = client.get_service(TAVILY)
        assert tavily is not None, "Tavily is not seeded (scripts/seed_tavily.py)"
        started_at = datetime.now(timezone.utc)

        turn = env.run_agent(AGENT, message=PROMPT, mode="agent", timeout_s=900)
        env.log("T5.1", f"job={turn['job_id']} status={turn['status']} agent_status={turn['agent_status']}")
        env.log("T5.1", f"text={str(turn['text'])[:600]!r}")
        env.log("T5.1", f"pending={[action.get('name') for action in turn['pending_actions']]}")
        assert turn["agent_status"] == "completed", turn["response"]

        searches = _searched_since(started_at, tavily.id)
        env.log("T5.2", f"web searches={[job.id for job in searches]}")
        assert searches, "the agent did not use web_search to find the GitHub MCP endpoint"

        nodes = (turn.get("workflow") or {}).get("nodes") or []
        env.log("T5.3", f"nodes={[(node.get('id'), node.get('kind'), node.get('service_id')) for node in nodes]}")
        service_ids = {node["service_id"] for node in nodes if node.get("service_id")}
        assert any(_is_github_mcp(service_id) for service_id in service_ids), "no GitHub MCP node in the workflow"
    env.log("T5", "PASS")


def test_spaine_connects_github_mcp() -> None:
    run()


if __name__ == "__main__":
    run()
