"""E2E: SDK conversations surface against the local platform stack.

One ``run_agent`` turn creates a conversation (``thread_id = chats.id``), then
the SDK client covers list / get / items / update / delete, plus Phase 2
tree (auto-title, 1/N siblings, fork) and mid-turn stub restore.

    python test/test_e2e_conversations.py
    pytest test/test_e2e_conversations.py -v -s

Needs socaity_backend (:8000) + inference stack (:8001) + SPAINE in the
catalog. Keys: see ``agentic_utils``.
"""
from __future__ import annotations

import sys
import threading
import time
from pathlib import Path
from uuid import uuid4

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import agentic_utils as env  # noqa: E402  (sets URL defaults before socaity import)

import socaity  # noqa: E402
from socaity.core.session import Session, use_session  # noqa: E402
from socaity.tools.agents import run_agent  # noqa: E402

PERSIST_TIMEOUT_S = 120.0

pytestmark = [
    pytest.mark.skipif(not env.backend_up(), reason=f"backend not reachable at {env.BACKEND}"),
    pytest.mark.skipif(not env.inference_up(), reason=f"APIPod gate not reachable at {env.GATE}"),
    pytest.mark.skipif(not env.rich_key(), reason="no test API key (SOCAITY_TEST_RICH_KEY / SOCAITY_API_KEY)"),
]

MARKER = f"conversations-e2e-{int(time.time())}"
PROMPT = f"Reply with exactly one short sentence that contains the token {MARKER}."
PING = f"Reply with exactly the word ping and the token {MARKER}-ping."
PONG = f"Reply with exactly the word pong and the token {MARKER}-pong."


def _wait_conversation(thread_id: str) -> None:
    """Chat history persistence is async after job FINISHED; poll for the row."""
    deadline = time.monotonic() + PERSIST_TIMEOUT_S
    while time.monotonic() < deadline:
        if socaity.get_conversation(thread_id) is not None:
            return
        time.sleep(2)
    raise AssertionError(f"conversation {thread_id} did not persist within {PERSIST_TIMEOUT_S}s")


def _item_text(item) -> str:
    return " ".join(
        part.text or ""
        for part in (item.parts or [])
        if getattr(part, "type", None) == "text"
    )


def _items_text(items) -> str:
    return " ".join(_item_text(item) for item in items)


def _wait_title(thread_id: str) -> str:
    deadline = time.monotonic() + PERSIST_TIMEOUT_S
    while time.monotonic() < deadline:
        chat = socaity.get_conversation(thread_id)
        if chat and chat.title:
            return chat.title
        time.sleep(2)
    raise AssertionError(f"conversation {thread_id} never received an auto-title")


def _role_items(items, role: str):
    return [item for item in items if item.role == role and item.kind == "message"]


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

        env.log("3", "query_conversations includes the thread")
        listed = socaity.query_conversations(limit=50)
        assert any(row.id == thread_id for row in listed), [row.id for row in listed[:10]]

        env.log("4", "items contain the turn")
        items = socaity.query_conversation_items(thread_id, branch="active")
        roles = [item.role for item in items]
        assert "user" in roles and "assistant" in roles, roles
        texts = _items_text(items)
        assert MARKER in texts, f"turn text missing marker {MARKER}: {texts[:300]!r}"
        all_items = socaity.query_conversation_items(thread_id, branch="all")
        assert len(all_items) >= len(items), (len(all_items), len(items))

        env.log("5", "auto-title after first reply (do not PATCH title first)")
        title = _wait_title(thread_id)
        env.log("5", f"title={title!r}")
        assert title and title.strip(), title
        assert title != PROMPT

        env.log("6", "1/N ping then sibling pong")
        users = _role_items(all_items, "user")
        assistants = _role_items(all_items, "assistant")
        first_user = users[0]
        first_asst = assistants[0]
        ping = run_agent(
            "spaine",
            message=PING,
            thread_id=thread_id,
            mode="chat",
            timeout_s=600,
        )
        assert ping["agent_status"] == "completed", ping["response"]
        _wait_conversation(thread_id)
        after_ping = socaity.query_conversation_items(thread_id, branch="all")
        ping_users = [item for item in _role_items(after_ping, "user") if MARKER + "-ping" in _item_text(item)]
        assert ping_users, _items_text(after_ping)
        ping_user = ping_users[0]
        pong = run_agent(
            "spaine",
            message=PONG,
            thread_id=thread_id,
            mode="chat",
            parent_item_id=ping_user.parent_id or first_asst.id,
            timeout_s=600,
        )
        assert pong["agent_status"] == "completed", pong["response"]
        _wait_conversation(thread_id)
        tree = socaity.query_conversation_items(thread_id, branch="all")
        ping_leaves = [item for item in _role_items(tree, "assistant") if MARKER + "-ping" in _item_text(item)]
        pong_leaves = [item for item in _role_items(tree, "assistant") if MARKER + "-pong" in _item_text(item)]
        assert ping_leaves and pong_leaves, _items_text(tree)

        env.log("7", "switch active leaf ping <-> pong")
        switched = socaity.update_conversation(thread_id, active_item_id=ping_leaves[0].id)
        assert switched is not None and switched.active_item_id == ping_leaves[0].id, switched
        active_ping = _items_text(socaity.query_conversation_items(thread_id, branch="active"))
        assert MARKER + "-ping" in active_ping
        assert MARKER + "-pong" not in active_ping
        socaity.update_conversation(thread_id, active_item_id=pong_leaves[0].id)
        active_pong = _items_text(socaity.query_conversation_items(thread_id, branch="active"))
        assert MARKER + "-pong" in active_pong

        env.log("8", "fork conversation from the sibling tree")
        forked = socaity.fork_conversation(thread_id)
        assert forked is not None and forked.id and forked.id != thread_id, forked
        _wait_conversation(forked.id)
        forked_items = socaity.query_conversation_items(forked.id, branch="all")
        assert len(forked_items) >= 2, len(forked_items)

        env.log("9", "PATCH title still works, then delete both chats")
        patched = socaity.update_conversation(thread_id, title=f"E2E {MARKER}")
        assert patched is not None and patched.title == f"E2E {MARKER}", patched
        assert socaity.delete_conversation(thread_id) is True
        assert socaity.delete_conversation(forked.id) is True
        assert socaity.get_conversation(thread_id) is None, "conversation still visible after delete"
    env.log("done", "PASS")


def test_conversations_end_to_end() -> None:
    run()


def test_mid_turn_stub_and_tool_parts() -> None:
    """Intake stub is visible while the job runs; completed parts include tools."""
    session = Session(api_key=env.rich_key(), backend_url=env.BACKEND)
    thread_id = str(uuid4())
    started: dict = {}
    finished: dict = {}

    def _turn() -> None:
        with use_session(session):
            finished["turn"] = run_agent(
                "spaine",
                message=(
                    "Search the catalog for image upscale services using query_services. "
                    f"Then reply in one short sentence that includes {MARKER}-tools."
                ),
                thread_id=thread_id,
                mode="agent",
                timeout_s=600,
                on_job_start=lambda job_id, _env: started.__setitem__("job_id", job_id),
            )

    with use_session(session):
        env.log("T2", f"submit agent turn thread={thread_id}")
        worker = threading.Thread(target=_turn, daemon=True)
        worker.start()
        for _ in range(100):
            if started.get("job_id"):
                break
            time.sleep(0.2)
        job_id = started.get("job_id")
        assert job_id, "on_job_start never fired"
        env.log("T2", f"job started {job_id}")

        stub = None
        deadline = time.monotonic() + 60
        while time.monotonic() < deadline:
            items = socaity.query_conversation_items(thread_id, branch="active")
            stub = next(
                (
                    item
                    for item in items
                    if item.role == "assistant" and item.status == "in_progress" and item.job_id == job_id
                ),
                None,
            )
            if stub:
                break
            time.sleep(1)
        assert stub is not None, "in_progress assistant stub with job_id missing mid-turn"
        live = socaity.get_job(job_id)
        assert live is not None, job_id
        env.log("T2", f"mid-turn stub={stub.id} job_status={getattr(live, 'status', None)}")

        worker.join(timeout=600)
        assert worker.is_alive() is False, "agent turn did not finish"
        turn = finished.get("turn")
        assert turn and turn["agent_status"] == "completed", turn
        _wait_conversation(thread_id)
        items = socaity.query_conversation_items(thread_id, branch="active")
        assistant = next((item for item in items if item.role == "assistant" and item.job_id == job_id), None)
        assert assistant is not None and assistant.status == "completed", assistant
        part_types = {getattr(part, "type", None) for part in (assistant.parts or [])}
        part_names = {getattr(part, "name", None) for part in (assistant.parts or [])}
        env.log("T2", f"completed parts types={part_types} names={part_names}")
        assert "tool_call" in part_types or "query_services" in part_names, (part_types, part_names)
        socaity.delete_conversation(thread_id)
    env.log("T2", "PASS")


if __name__ == "__main__":
    run()
    test_mid_turn_stub_and_tool_parts()
