"""PyPI publish gate: in-process invariants, then the stacked platform e2e.

Run when the local stack is up (backend :8000, gate :8001, SPAINE in catalog):

    pytest test/bundle/test_core.py -v -s

Not collected by default ``pytest`` (see ``norecursedirs``). Do not add
manual official-service tests or the Replicate zoo here.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

TEST_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TEST_DIR))

import agentic_utils as env  # noqa: E402

from socaity import SocaityClient  # noqa: E402

import test_e2e_catalog as catalog  # noqa: E402
import test_e2e_files as files  # noqa: E402
import test_e2e_jobs as jobs  # noqa: E402
import test_e2e_conversations as conversations  # noqa: E402
import test_e2e_agent_hitl as hitl  # noqa: E402
import test_e2e_wait_cancel as wait_cancel  # noqa: E402
import test_e2e_workflow_repair as workflow_repair  # noqa: E402


def test_core_request_invariants() -> None:
    """Always-on: run_agent body rules and ChatSocaity request shape."""
    client = SocaityClient(api_key="sk_test_core")
    with pytest.raises(ValueError, match="message"):
        client.run_agent("spaine")
    with pytest.raises(ValueError, match="thread_id"):
        client.run_agent("spaine", continue_turn=True)
    with pytest.raises(ValueError, match="no messages"):
        client.run_agent("spaine", message="hi", thread_id="chat-1", continue_turn=True)
    with pytest.raises(ValueError, match="supersede"):
        client.run_agent(
            "spaine",
            thread_id="chat-1",
            continue_turn=True,
            supersedes_job_id="job-1",
        )

    pytest.importorskip("langchain_core")
    from langchain_core.messages import HumanMessage
    from socaity.integrations.langchain import ChatSocaity

    model = ChatSocaity(model="https://example.invalid/chat", reasoning_effort="low")
    request = model._request([HumanMessage(content="hi")], None)
    assert request["reasoning_effort"] == "low"
    assert request["messages"][0]["content"] == "hi"


@pytest.mark.skipif(not env.backend_up(), reason=f"backend not reachable at {env.BACKEND}")
@pytest.mark.skipif(not env.inference_up(), reason=f"APIPod gate not reachable at {env.GATE}")
@pytest.mark.skipif(not env.api_key(), reason=env.missing_env("SOCAITY_API_KEY") or "no SOCAITY_API_KEY")
def test_core_platform_stack() -> None:
    """Ladder: catalog → files → jobs → conversations → HIT → wait/cancel → repair."""
    env.log("core", "catalog")
    catalog.run()
    env.log("core", "files")
    files.run()
    env.log("core", "jobs (one flux via run_service)")
    jobs.run()
    env.log("core", "conversations")
    conversations.run()
    env.log("core", "mid-turn stub + tool parts")
    conversations.test_mid_turn_stub_and_tool_parts()
    env.log("core", "HIT")
    hitl.run()
    env.log("core", "wait-cancel")
    wait_cancel.run()
    env.log("core", "workflow repair")
    workflow_repair.run()
    env.log("core", "PASS")
