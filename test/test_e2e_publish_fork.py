"""E2E: publish, second-user fork + revision, run, revert.

Owner (rich key) publishes a workflow. The second user (poor key) modifies it
through SPAINE, which forks it via blueprint persistence, runs the fork, then
reverts the revision and checks the document is back to the original content.

    python test/test_e2e_publish_fork.py
    pytest test/test_e2e_publish_fork.py -v -s

Needs socaity_backend (:8000) + inference stack (:8001) + SPAINE in the
catalog. Keys: see ``agentic_utils`` (this test needs both users).
"""
from __future__ import annotations

import sys
import time
from pathlib import Path
from uuid import uuid4

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import agentic_utils as env  # noqa: E402  (sets URL defaults before socaity import)

import socaity  # noqa: E402
from socaity.core.session import Session, use_session  # noqa: E402

AGENT = "spaine"

pytestmark = [
    pytest.mark.skipif(not env.backend_up(), reason=f"backend not reachable at {env.BACKEND}"),
    pytest.mark.skipif(not env.inference_up(), reason=f"APIPod gate not reachable at {env.GATE}"),
    pytest.mark.skipif(not env.rich_key(), reason="no test API key (SOCAITY_TEST_RICH_KEY / SOCAITY_API_KEY)"),
    pytest.mark.skipif(not env.poor_key(), reason="no second-user key (SOCAITY_TEST_POOR_KEY)"),
]

TITLE = f"Publish fork probe {int(time.time())}"
BASE_DOC = {
    "id": f"wf_{uuid4()}",
    "title": TITLE,
    "goal": "Wait shortly, then pass the text input through.",
    "nodes": [
        {"id": "nd_input", "kind": "builtin", "title": "input"},
        {"id": "nd_wait", "kind": "builtin", "title": "wait", "config": {"op": "wait", "seconds": 2}},
        {"id": "nd_output", "kind": "builtin", "title": "output"},
    ],
    "edges": [
        {"id": "ed_in_wait", "source": "nd_input", "target": "nd_wait", "map": "text"},
        {"id": "ed_wait_out", "source": "nd_wait", "target": "nd_output"},
    ],
}


def run() -> None:
    owner = Session(api_key=env.rich_key(), backend_url=env.BACKEND)
    with use_session(owner):
        saved = env.sdk().upsert_workflow(BASE_DOC, slug=f"publish-fork-{int(time.time())}", message="publish-fork base")
        wf_id = saved.workflow.id
        # Publish requires a validated revision; a completed run validates it.
        warmup = env.run_workflow(wf_id, inputs={"text": "warmup"}, timeout_s=180)
        env.log("T2B", f"owner warmup run status={(warmup.get('result') or {}).get('status')}")
        published = env.sdk().publish_workflow(wf_id)
        env.log("T2B", f"owner saved+published {wf_id} (published={published is not None})")
        assert published is not None, "publish failed"

    second = Session(api_key=env.poor_key(), backend_url=env.BACKEND)
    with use_session(second):
        fetched = env.sdk().get_workflow(wf_id)
        assert fetched is not None, "second user cannot see the published workflow"
        document = fetched.document.model_dump(mode="json", exclude_none=True)
        env.log("T2B", f"second user fetched published workflow: {fetched.title}")

        turn = env.run_agent(
            AGENT,
            message=(
                "Modify the draft workflow with exactly one tool call and nothing else: "
                "workflow_add_node with kind='builtin', node_id='nd_note', title='note', "
                "config={\"op\": \"identity\"}. Then reply with the single word: done."
            ),
            mode="plan",
            workflow=document,
            timeout_s=600,
        )
        env.log("T2B", f"plan turn job={turn['job_id']} agent_status={turn.get('agent_status')}")
        snapshot_nodes = [n.get("id") for n in ((turn.get("workflow") or {}).get("nodes") or [])]
        env.log("T2B", f"snapshot nodes: {snapshot_nodes}")

        fork = None
        for _ in range(15):
            mine = env.sdk().query_workflows(filters=["visibility:eq:mine"], limit=50)
            fork = next((w for w in mine if w.title == TITLE and w.id != wf_id), None)
            if fork is not None:
                break
            time.sleep(2)
        assert fork is not None, "no fork appeared for the second user"
        env.log("T2B", f"fork id={fork.id}")
        fork_revisions = env.sdk().query_workflow_revisions(fork.id)
        env.log("T2B", f"fork revisions: {[(r.id, r.message) for r in fork_revisions]}")
        fork_doc = env.sdk().get_workflow(fork.id).document
        env.log("T2B", f"fork nodes: {[n.id for n in fork_doc.nodes]}")

        fork_run = env.run_workflow(fork.id, inputs={"text": "hello"}, timeout_s=180)
        result = fork_run.get("result") or {}
        env.log("T2B", f"fork run job={fork_run['job_id']} status={fork_run['status']} run_status={result.get('status')}")
        assert result.get("status") == "completed", result

        # Revert to the fork's base revision (the copied original content).
        base_revision = fork_revisions[-1]
        reverted = env.sdk().revert_workflow(fork.id, revision_id=base_revision.id)
        assert reverted is not None, "revert failed"
        after = env.sdk().get_workflow(fork.id).document
        env.log("T2B", f"after revert nodes: {[n.id for n in after.nodes]}")
        original_ids = sorted(n["id"] for n in BASE_DOC["nodes"])
        assert sorted(n.id for n in after.nodes) == original_ids, "revert did not restore the original document"
    env.log("done", "PASS")


def test_publish_fork() -> None:
    run()


if __name__ == "__main__":
    run()
