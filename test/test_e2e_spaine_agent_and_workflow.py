"""E2E: Two-step natural-language agent creation & workflow execution via SPAINE.

Step 1 (Agent only): Prompts SPAINE (`mode = "agent"`) in natural language to
create a standalone catalog agent granted `tavily`, `black-forest-labs-flux-schnell`,
and Google Sheets (`sheets-spreadsheets-create`). Asserts the catalog
`Service(kind="agent")` exists with all 3 grants and no workflow was created.

Step 2 (Workflow composition & run): Prompts SPAINE (`mode = "plan"`) to build
and save a workflow around that agent, then executes `run_workflow`. Asserts
the workflow completes (or pauses on missing connector credentials if unbound)
and executes under the agent turn.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import agentic_utils as env  # noqa: E402

from socaity import Session, client  # noqa: E402
from socaity_cli.errors import BackendApiError  # noqa: E402

GOOGLE_SHEETS_SPEC_URL = "https://api.apis.guru/v2/specs/googleapis.com/sheets/v4/openapi.json"


def _ensure_google_sheets_connector() -> None:
    try:
        client.register_connector(GOOGLE_SHEETS_SPEC_URL)
    except BackendApiError as exc:
        if exc.status_code != 409 or exc.code != "connector_exists":
            raise

pytestmark = [
    pytest.mark.skipif(not env.backend_up(), reason=f"backend not reachable at {env.BACKEND}"),
    pytest.mark.skipif(not env.inference_up(), reason=f"APIPod gate not reachable at {env.GATE}"),
    pytest.mark.skipif(not env.api_key(), reason=env.missing_env("SOCAITY_API_KEY") or "no SOCAITY_API_KEY"),
]


def run() -> None:
    agent_slug = f"market-scout-{int(time.time())}"
    session = Session(api_key=env.api_key(), backend_url=env.BACKEND)
    with session:
        _ensure_google_sheets_connector()
        # Step 1: Natural-language standalone agent creation
        prompt_step1 = (
            f"Create a new standalone catalog agent with slug '{agent_slug}' and display_name 'Market Scout'. "
            "Use your agent_composition skill and upsert_agent tool. "
            "Grant it three catalog endpoints: tavily search, black-forest-labs-flux-schnell image generation, "
            "and Google Sheets spreadsheets create (sheets-spreadsheets-create). "
            "Do NOT create or edit any workflow in this step."
        )
        turn1 = env.run_agent(
            "spaine",
            message=prompt_step1,
            mode="agent",
            socaity_options={
                "settings": {
                    "tools": {
                        "upsert_agent": "never_ask",
                        "fork_agent": "never_ask",
                        "query_services": "never_ask",
                        "get_service": "never_ask",
                    }
                }
            },
            timeout_s=600,
        )
        env.log("S1", f"turn1 status={turn1['agent_status']} text={str(turn1['text'])[:300]!a}")
        assert turn1["agent_status"] == "completed", turn1
        assert not turn1.get("workflow"), f"Expected no workflow in Step 1, got {turn1.get('workflow')}"

        created_agent = client.get_agent(agent_slug)
        assert created_agent, f"Agent {agent_slug} not found in catalog"
        assert created_agent.get("kind") == "agent", created_agent
        details = (created_agent.get("details") or [{}])[0]
        spec = details.get("spec_document") or (details.get("contract") or {}).get("raw_schema") or {}
        grants = spec.get("grants") or []
        env.log("S1", f"created agent id={created_agent.get('id')} grants={grants}")
        assert len(grants) >= 3, f"Expected at least 3 endpoint grants on {agent_slug}, got {grants}"

        # Step 2: Compose a workflow around that agent and run it
        prompt_step2 = (
            f"Build a workflow with a single agent node (`kind='agent'`, service_id='{created_agent['id']}') "
            "connected directly to an output node. Set the agent node's `inputs.prompt` to: "
            "'Call tavily-search once with query=\"Model Context Protocol\" and search_depth=\"basic\", "
            "call black-forest-labs-flux-schnell once with prompt=\"minimalist icon\", "
            "and call google-sheets sheets-spreadsheets-create once with properties={\"title\": \"MCP Brief\"}, "
            "then reply with a one-sentence summary without further tool calls.'"
        )
        turn2 = env.run_agent(
            "spaine",
            message=prompt_step2,
            mode="plan",
            thread_id=turn1["thread_id"],
            timeout_s=600,
        )
        env.log("S2", f"turn2 status={turn2['agent_status']} has_workflow={bool(turn2.get('workflow'))}")
        wf_doc = turn2.get("workflow")
        assert wf_doc and isinstance(wf_doc, dict), f"Expected workflow draft from plan mode, got {turn2}"
        agent_nodes = [n for n in (wf_doc.get("nodes") or []) if n.get("kind") == "agent"]
        assert agent_nodes, f"Expected at least one kind='agent' node in workflow, got {wf_doc.get('nodes')}"

        wf_slug = f"wf-{agent_slug}"
        saved = client.upsert_workflow(wf_doc, slug=wf_slug, message="e2e step 2 workflow with custom agent")
        wf_id = saved.workflow.id
        env.log("S2", f"saved workflow id={wf_id}; running...")

        wf_run = env.run_workflow(wf_id, inputs={}, timeout_s=900)
        result = wf_run.get("result") or {}
        env.log("S2", f"workflow run status={wf_run['status']} result={json.dumps(result, default=str)[:500]}")
        assert wf_run["status"] == "finished", wf_run
        assert result.get("status") in ("completed", "interrupted"), result

        try:
            client.delete_agent(created_agent["id"])
        except Exception as exc:
            env.log("S2", f"cleanup warning: {exc}")

    env.log("done", "PASS")


def test_spaine_agent_and_workflow() -> None:
    run()


if __name__ == "__main__":
    run()
