"""E2E: SDK conversations surface against the local platform stack.

One ``run_agent`` turn creates a conversation (``thread_id = chats.id``), then
the SDK client covers list / get / items / update / delete.

    python test/test_e2e_conversations.py
    pytest test/test_e2e_conversations.py -v -s

Needs socaity_backend (:8000) + inference stack (:8001) + SPAINE in the
catalog. Keys: see ``agentic_utils``.
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import agentic_utils as env  # noqa: E402  (sets URL defaults before socaity import)

import socaity  # noqa: E402
from socaity.core.session import Session, use_session  # noqa: E402
from socaity.tools.agents import run_agent  # noqa: E402

PERSIST_TIMEOUT_S = 120.0

pytestmark = [
    pytest.mark.skipif(not env.backend_up(), reason=f"backend not reachable at {env.BACKEND}"),
    pytest.mark.skipif(not env.inference_up(), reason=f"inference gateway not reachable at {env.INFERENCE}"),
    pytest.mark.skipif(not env.rich_key(), reason="no test API key (SOCAITY_TEST_RICH_KEY / SOCAITY_API_KEY)"),
]

MARKER = f"conversations-e2e-{int(time.time())}"
PROMPT = f"Reply with exactly one short sentence that contains the token {MARKER}."


def _wait_conversation(thread_id: str) -> None:
    """Chat history persistence is async after job FINISHED; poll for the row."""
    deadline = time.monotonic() + PERSIST_TIMEOUT_S
    while time.monotonic() < deadline:
        if socaity.get_conversation(thread_id) is not None:
            return
        time.sleep(2)
    raise AssertionError(f"conversation {thread_id} did not persist within {PERSIST_TIMEOUT_S}s")


def run() -> None:
    session = Session(api_key=env.rich_key(), backend_url=env.BACKEND)
    with use_session(session):
        env.log("1", "run one agent turn (chat mode)")
        turn = run_agent("spaine", message=PROMPT, mode="chat", timeout_s=600)
        thread_id = turn["thread_id"]
        env.log("1", f"job={turn['job_id']} agent_status={turn['agent_status']} thread={thread_id}")
        assert turn["agent_status"] == "completed", turn["response"]
        assert thread_id, "agent turn returned no thread_id"

        env.log("2", "conversation row exists for the thread")
        _wait_conversation(thread_id)
        chat = socaity.get_conversation(thread_id)
        assert chat is not None and chat.id == thread_id, chat

        env.log("3", "list_conversations includes the thread")
        listed = socaity.list_conversations(limit=50)
        assert any(row.id == thread_id for row in listed), [row.id for row in listed[:10]]

        env.log("4", "items contain the turn")
        items = socaity.list_conversation_items(thread_id, branch="active")
        roles = [item.role for item in items]
        assert "user" in roles and "assistant" in roles, roles
        texts = " ".join(
            part.text or ""
            for item in items
            for part in (item.parts or [])
            if getattr(part, "type", None) == "text"
        )
        assert MARKER in texts, f"turn text missing marker {MARKER}: {texts[:300]!r}"
        all_items = socaity.list_conversation_items(thread_id, branch="all")
        assert len(all_items) >= len(items), (len(all_items), len(items))

        env.log("5", "update + delete")
        patched = socaity.update_conversation(thread_id, title=f"E2E {MARKER}")
        assert patched is not None and patched.title == f"E2E {MARKER}", patched
        assert socaity.delete_conversation(thread_id) is True
        assert socaity.get_conversation(thread_id) is None, "conversation still visible after delete"
    env.log("done", "PASS")


def test_conversations_end_to_end() -> None:
    run()


if __name__ == "__main__":
    run()
