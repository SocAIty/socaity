"""E2E Test 3: agent image job (flux-schnell) then qwen3.8 VLM describe.

Runs through the local platform stack (backend + gateway + engines). The
engines process must have ``AGENT_ENGINE_DSN`` so LangGraph uses
``PostgresSaver``. Do not run this against a standalone SPAINE
``InMemorySaver`` process.

    python test/test_e2e_agent_image_vlm.py
    pytest test/test_e2e_agent_image_vlm.py -v -s

Keys: see ``agentic_utils``.
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
GENERATE_TIMEOUT_S = 1800.0
DESCRIBE_TIMEOUT_S = 600.0
FLUX = "black-forest-labs-flux-schnell"
MARKER = f"image-vlm-e2e-{int(time.time())}"
GENERATE = (
    "Use run_service on "
    f"{FLUX} "
    "with prompt: an image of a monkey 3d clipart. "
    f"After the job finishes, reply in one short sentence that includes {MARKER}."
)
LIST = (
    "Use query_jobs with limit 10 to list my last 10 jobs. "
    "Reply with each job id and status. "
    f"Include the token {MARKER}-jobs."
)
DESCRIBE = (
    "Describe the composition of the image you just generated. "
    "Name the subject, layout, and colors. "
    "Do not say you cannot see the image. "
    f"Include the token {MARKER}-vlm in the reply."
)
BLIND = (
    "cannot see",
    "can't see",
    "can not see",
    "unable to view",
    "unable to see",
    "don't have access to the image",
    "do not have access to the image",
    "as a text-based",
    "i cannot view",
    "i can't view",
    "no image",
)

pytestmark = [
    pytest.mark.skipif(not env.backend_up(), reason=f"backend not reachable at {env.BACKEND}"),
    pytest.mark.skipif(not env.inference_up(), reason=f"APIPod gate not reachable at {env.GATE}"),
    pytest.mark.skipif(not env.rich_key(), reason="no test API key (SOCAITY_TEST_RICH_KEY / SOCAITY_API_KEY)"),
]


def _wait_conversation(thread_id: str) -> None:
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


def _tool_results(items, name: str) -> list:
    """Named ``tool_result`` parts. Same index the Run panel and job bubbles read."""
    hits = []
    for item in items:
        if item.role != "assistant":
            continue
        for part in item.parts or []:
            if getattr(part, "type", None) != "tool_result":
                continue
            if getattr(part, "name", None) != name:
                continue
            hits.append((item, part, getattr(part, "output", None)))
    return hits


def _run_service_results(items) -> list:
    hits = []
    for item, part, output in _tool_results(items, "run_service"):
        if isinstance(output, dict) and output.get("job_id"):
            hits.append((item, part, output))
    return hits


def _job_ids(output) -> list[str]:
    rows = output if isinstance(output, list) else []
    ids = []
    for row in rows:
        if isinstance(row, dict) and row.get("id"):
            ids.append(row["id"])
    return ids


def _files_of(output: dict) -> list[str]:
    files = output.get("files") or []
    urls = [item for item in files if isinstance(item, str) and item.startswith("http")]
    result = output.get("result")
    if isinstance(result, str) and result.startswith("http"):
        urls.append(result)
    return urls


def run() -> None:
    session = Session(api_key=env.rich_key(), backend_url=env.BACKEND)
    with use_session(session):
        env.log("T3.1", f"generate monkey clipart via {FLUX}")
        first = run_agent("spaine", message=GENERATE, mode="agent", timeout_s=GENERATE_TIMEOUT_S)
        thread_id = first["thread_id"]
        env.log("T3.1", f"job={first['job_id']} agent_status={first['agent_status']} thread={thread_id}")
        assert first["agent_status"] == "completed", first["response"]
        assert thread_id, "agent turn returned no thread_id"
        _wait_conversation(thread_id)

        items = socaity.query_conversation_items(thread_id, branch="active")
        results = _run_service_results(items)
        assert results, f"no run_service tool_result with job_id (bubble/panel data missing): {items}"
        _item, _part, output = results[0]
        child_job_id = output["job_id"]
        env.log("T3.1", f"child_job={child_job_id} status={output.get('status')}")

        tracked = socaity.get_job(child_job_id)
        assert tracked is not None, f"get_job missed child {child_job_id}"
        status = (getattr(tracked, "status", None) or output.get("status") or "").lower()
        assert status in ("finished", "completed", "success"), (
            child_job_id,
            status,
            getattr(tracked, "status", None),
        )
        files = _files_of(output)
        assert files, f"run_service returned no image URLs: {output}"
        assert (output.get("status") or "").lower() in ("finished", "completed", "success"), output
        env.log("T3.1", f"tracked status={status} files={len(files)}")

        env.log("T3.2", "list last 10 jobs via query_jobs")
        listed = run_agent(
            "spaine",
            message=LIST,
            thread_id=thread_id,
            mode="agent",
            timeout_s=DESCRIBE_TIMEOUT_S,
        )
        assert listed["agent_status"] == "completed", listed["response"]
        _wait_conversation(thread_id)
        after_list = socaity.query_conversation_items(thread_id, branch="active")
        list_parts = _tool_results(after_list, "query_jobs")
        assert list_parts, f"query_jobs tool_result missing (tool not bound or call failed): {after_list}"
        list_output = list_parts[0][2]
        listed_ids = _job_ids(list_output)
        env.log("T3.2", f"query_jobs n={len(listed_ids)}")
        assert listed_ids, f"query_jobs returned no jobs: {list_output!r}"
        assert child_job_id in listed_ids, (child_job_id, listed_ids)
        sdk_jobs = socaity.query_jobs(limit=10)
        sdk_ids = {getattr(job, "id", None) for job in sdk_jobs}
        assert child_job_id in sdk_ids, (child_job_id, sdk_ids)

        env.log("T3.3", "describe composition (qwen3.8 VLM on the image URL)")
        second = run_agent(
            "spaine",
            message=DESCRIBE,
            thread_id=thread_id,
            mode="agent",
            timeout_s=DESCRIBE_TIMEOUT_S,
        )
        assert second["agent_status"] == "completed", second["response"]
        _wait_conversation(thread_id)
        after = socaity.query_conversation_items(thread_id, branch="active")
        assistants = [item for item in after if item.role == "assistant" and item.kind == "message"]
        describe_text = " ".join(_item_text(item) for item in assistants[-1:])
        if MARKER + "-vlm" not in describe_text:
            describe_text = " ".join(_item_text(item) for item in assistants)
        env.log("T3.3", f"describe={describe_text[:400]!r}")
        assert describe_text.strip(), "empty VLM reply"
        lowered = describe_text.lower()
        assert not any(phrase in lowered for phrase in BLIND), f"model claimed it cannot see the image: {describe_text!r}"
        visual = ("monkey", "color", "colour", "composition", "background", "clipart", "subject")
        assert any(word in lowered for word in visual), f"reply is not a visual description: {describe_text!r}"

        socaity.delete_conversation(thread_id)
    env.log("T3", "PASS")


def test_agent_image_then_vlm_describe() -> None:
    run()


if __name__ == "__main__":
    run()
