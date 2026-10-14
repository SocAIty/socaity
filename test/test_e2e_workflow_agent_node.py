"""E2E: workflow inline AgentNode and structured output.

Saves and runs a workflow containing an inline AgentNode (service_id="spaine")
with an output_schema ({"city", "country"}) and an outgoing edge mapping
data.city into a downstream node.

Verifies:
- SdkNodeRunner dispatches via run_agent
- normalizes {text, data, files} so JMESPath `data.city` resolves downstream
- does not leak a standalone `chats` row for the workflow step turn
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path
from uuid import uuid4

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import agentic_utils as env  # noqa: E402

from socaity import Session, client  # noqa: E402

pytestmark = [
    pytest.mark.skipif(not env.backend_up(), reason=f"backend not reachable at {env.BACKEND}"),
    pytest.mark.skipif(not env.inference_up(), reason=f"APIPod gate not reachable at {env.GATE}"),
    pytest.mark.skipif(not env.api_key(), reason=env.missing_env("SOCAITY_API_KEY") or "no SOCAITY_API_KEY"),
]


def _build_workflow_doc() -> dict:
    return {
        "id": f"wf_{uuid4()}",
        "title": "Inline AgentNode Structured Output E2E",
        "goal": "Extract capital city and country as structured JSON and pass city downstream",
        "nodes": [
            {"id": "nd_input", "kind": "builtin", "title": "input"},
            {
                "id": "nd_agent",
                "kind": "agent",
                "title": "Extract City & Country",
                "service_id": "spaine",
                "system_prompt": (
                    "Extract the city and country that answer the user's question. "
                    "Return valid JSON matching the output schema."
                ),
                "output_schema": {
                    "type": "object",
                    "properties": {
                        "city": {"type": "string"},
                        "country": {"type": "string"},
                    },
                    "required": ["city", "country"],
                },
                "inputs": {},
            },
            {"id": "nd_output", "kind": "builtin", "title": "output"},
        ],
        "edges": [
            {
                "id": "ed_in_agent",
                "source": "nd_input",
                "target": "nd_agent",
                "port": "prompt",
                "map": "question",
            },
            {
                "id": "ed_agent_out",
                "source": "nd_agent",
                "target": "nd_output",
                "port": "city",
                "map": "data.city",
            },
        ],
    }


def run() -> None:
    doc = _build_workflow_doc()
    slug = f"agent-node-e2e-{int(time.time())}"

    session = Session(api_key=env.api_key(), backend_url=env.BACKEND)
    with session:
        chats_before = {c.id for c in client.query_conversations(limit=50)}

        saved = client.upsert_workflow(doc, slug=slug, message="e2e inline agent node")
        assert saved and saved.workflow, "workflow upsert failed"
        wf_id = saved.workflow.id
        env.log("T2", f"saved workflow id={wf_id} slug={slug}")

        wf_run = env.run_workflow(wf_id, inputs={"question": "What is the capital of France?"}, timeout_s=600)
        result = wf_run.get("result") or {}
        env.log("T2", f"run status={wf_run['status']} result={json.dumps(result, default=str)[:600]}")
        assert wf_run["status"] == "finished", wf_run
        assert result.get("status") == "completed", result

        outputs = result.get("outputs")
        env.log("T2", f"outputs={outputs}")
        assert "paris" in json.dumps(outputs, default=str).lower(), f"Expected 'Paris' in output, got {outputs}"

        chats_after = {c.id for c in client.query_conversations(limit=50)}
        leaked = chats_after - chats_before
        assert not leaked, f"Workflow AgentNode step leaked standalone chats rows: {leaked}"

    env.log("done", "PASS")


def test_workflow_agent_node() -> None:
    run()


if __name__ == "__main__":
    run()
