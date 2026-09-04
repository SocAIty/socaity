"""E2E: agent HITL multiple choice through the full platform stack.

Part A: run agent -> interrupted -> resume with decisions on the same thread.
Part B: run agent -> interrupted -> list interrupts on the backend, resolve via
endpoint, poll the enqueued continue job.

    python test/test_e2e_agent_hitl.py
    pytest test/test_e2e_agent_hitl.py -v -s

Needs socaity_backend (:8000) + inference stack (:8001) + SPAINE in the
catalog. Keys: see ``agentic_utils``.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import agentic_utils as env  # noqa: E402  (sets URL defaults before socaity import)

import socaity  # noqa: E402
from socaity.core.session import Session, use_session  # noqa: E402
from socaity.tools.agents import run_agent  # noqa: E402

PROMPT = "Give me a multiple choice with 5 recipes and let me pick one."

pytestmark = [
    pytest.mark.skipif(not env.backend_up(), reason=f"backend not reachable at {env.BACKEND}"),
    pytest.mark.skipif(not env.inference_up(), reason=f"APIPod gate not reachable at {env.GATE}"),
    pytest.mark.skipif(not env.rich_key(), reason="no test API key (SOCAITY_TEST_RICH_KEY / SOCAITY_API_KEY)"),
]


def start_interrupted_turn(tag: str) -> dict:
    result = run_agent("spaine", message=PROMPT, mode="chat", timeout_s=600)
    env.log(tag, f"job={result['job_id']} status={result['status']} agent_status={result['agent_status']}")
    env.log(tag, f"thread={result['thread_id']} text={str(result['text'])[:200]!r}")
    assert result["agent_status"] == "interrupted", f"expected interrupted turn, got: {result['response']}"
    assert result["pending_actions"], "interrupted turn without pending_actions"
    for action in result["pending_actions"]:
        env.log(tag, f"pending action id={action['id']} name={action['name']} allowed={action.get('allowed_decisions')}")
        env.log(tag, f"  args={str(action.get('arguments'))[:400]}")
    return result


def part_a_resume_with_decisions() -> None:
    env.log("A", "start turn expecting multiple-choice HIT")
    first = start_interrupted_turn("A")
    action = first["pending_actions"][0]
    decision_type = "respond" if "respond" in (action.get("allowed_decisions") or []) else "approve"
    decisions = [{
        "interrupt_row_id": action["id"],
        "type": decision_type,
        "message": "I pick option 2." if decision_type == "respond" else None,
    }]
    decisions = [{k: v for k, v in d.items() if v is not None} for d in decisions]
    env.log("A", f"resume thread={first['thread_id']} decision={decisions[0]}")
    second = run_agent("spaine", thread_id=first["thread_id"], decisions=decisions, timeout_s=600)
    env.log("A", f"resumed job={second['job_id']} agent_status={second['agent_status']}")
    env.log("A", f"text={str(second['text'])[:400]!r}")
    assert second["agent_status"] == "completed", f"resume did not complete: {second['response']}"
    assert second["text"], "no assistant text after resume"
    env.log("A", "PASS")


def part_b_backend_interrupts() -> None:
    env.log("B", "start second turn, resolve via backend interrupt endpoint")
    first = start_interrupted_turn("B")
    pending = socaity.query_interrupts()
    env.log("B", f"backend pending interrupts: {len(pending)}")
    row_ids = {a["id"] for a in first["pending_actions"]}
    mine = [r for r in pending if str(r.id) in row_ids]
    assert mine, f"stream row ids {row_ids} not in backend pending list {[str(r.id) for r in pending]}"
    row = mine[0]
    decision = "respond" if "respond" in (row.allowed_decisions or []) else "approve"
    result = socaity.resolve_interrupt(
        str(row.id),
        decision=decision,
        message="I pick option 3." if decision == "respond" else None,
    )
    env.log("B", f"resolved batch_complete={result.batch_complete} job={getattr(result.job, 'id', None)}")
    assert result.batch_complete, "batch not complete after resolving the only action"
    assert result.job is not None, "no continue job enqueued"
    job = env.poll_job(str(result.job.id), api_key=env.rich_key())
    env.log("B", f"continue job status={job.get('status')}")
    response = job.get("result") if isinstance(job.get("result"), dict) else {}
    text = ((response.get("choices") or [{}])[0].get("message") or {}).get("content")
    env.log("B", f"final text={str(text)[:400]!r}")
    assert (job.get("status") or "").lower() == "finished", job
    assert text, "no assistant text on continue job"
    env.log("B", "PASS")


def run() -> None:
    session = Session(api_key=env.rich_key(), backend_url=env.BACKEND)
    with use_session(session):
        part_a_resume_with_decisions()
        part_b_backend_interrupts()
    env.log("done", "PASS")


def test_agent_hitl() -> None:
    run()


if __name__ == "__main__":
    run()
