"""E2E: publish, pin resolution (published vs latest_valid vs explicit revision_id),
second-user fork + revision, run, revert.

    python test/test_e2e_publish_fork.py
    pytest test/test_e2e_publish_fork.py -v -s

Needs socaity_backend (:8000) + inference stack (:8001) + SPAINE in the
catalog. Keys: see ``agentic_utils`` (this test needs both users).
"""
from __future__ import annotations

import copy
import sys
import time
from pathlib import Path
from uuid import uuid4

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import agentic_utils as env  # noqa: E402  (sets URL defaults before socaity import)

import socaity  # noqa: E402
from socaity import Session, client  # noqa: E402

AGENT = "spaine"

pytestmark = [
    pytest.mark.skipif(not env.backend_up(), reason=f"backend not reachable at {env.BACKEND}"),
    pytest.mark.skipif(not env.inference_up(), reason=f"APIPod gate not reachable at {env.GATE}"),
    pytest.mark.skipif(not env.api_key(), reason=env.missing_env("SOCAITY_API_KEY") or "no SOCAITY_API_KEY"),
    pytest.mark.skipif(not env.poor_key(), reason=env.missing_env("SOCAITY_POOR_API_KEY") or "no SOCAITY_POOR_API_KEY"),
]

TITLE = f"Publish fork probe {int(time.time())}"
BASE_DOC = {
    "id": f"wf_{uuid4()}",
    "title": TITLE,
    "goal": "Wait shortly, then pass the text input through.",
    "nodes": [
        {"id": "nd_input", "kind": "transform", "title": "input", "op": "identity"},
        {"id": "nd_wait", "kind": "control", "title": "Wait", "config": {"op": "wait", "seconds": 1}},
        {"id": "nd_output", "kind": "transform", "title": "output", "op": "identity"},
    ],
    "edges": [
        {"id": "ed_in_wait", "source": "nd_input", "target": "nd_wait", "map": "text"},
        {"id": "ed_wait_out", "source": "nd_wait", "target": "nd_output"},
    ],
}


def run() -> None:
    owner = Session(api_key=env.api_key(), backend_url=env.BACKEND)
    with owner:
        saved = client.upsert_workflow(BASE_DOC, slug=f"publish-fork-{int(time.time())}", message="publish-fork base")
        wf_id = saved.workflow.id
        rev1 = saved.revision.id
        # Publish requires a validated revision; a completed run validates it.
        warmup = env.run_workflow(wf_id, inputs={"text": "warmup"}, timeout_s=180)
        warmup_res = warmup.get("result") or {}
        env.log("T2B", f"owner warmup run status={warmup_res.get('status')}")
        assert warmup_res.get("status") == "completed", warmup
        published = client.publish_workflow(wf_id)
        env.log("T2B", f"owner saved+published {wf_id} (published={published is not None})")
        assert published is not None, "publish failed"
        assert published.published_revision_id == rev1

        # Save and successfully run a second owner revision, and do NOT publish it.
        v2_doc = copy.deepcopy(saved.document.model_dump(mode="json", exclude_none=True))
        v2_doc.get("metadata", {}).pop("content_hash", None)
        v2_doc["edges"] = [
            {"id": "ed_in_wait", "source": "nd_input", "target": "nd_wait", "map": "text"},
            {"id": "ed_wait_out", "source": "nd_wait", "target": "nd_output", "map": "[`v2`, @]"},
        ]
        saved_v2 = client.upsert_workflow(v2_doc, message="owner v2 unpublished")
        rev2 = saved_v2.revision.id
        assert rev2 != rev1

        v2_run = env.run_workflow(wf_id, revision_id=rev2, inputs={"text": "validate-v2"}, timeout_s=180)
        v2_res = v2_run.get("result") or {}
        assert v2_res.get("status") == "completed", v2_run

        after_v2 = client.get_workflow(wf_id)
        assert after_v2.published_revision_id == rev1
        assert after_v2.latest_valid_revision_id == rev2

        # Owner runs with no revision_id -> uses new valid revision (rev2).
        owner_default = env.run_workflow(wf_id, inputs={"text": "owner-latest"}, timeout_s=180)
        owner_default_res = owner_default.get("result") or {}
        assert owner_default_res.get("status") == "completed", owner_default
        owner_default_row = client.get_workflow_run(owner_default_res["workflow_run_id"])
        assert owner_default_row.revision_id == rev2
        assert owner_default_res.get("outputs", {}).get("nd_output") == ["v2", "owner-latest"]

        # Pass revision_id explicitly -> runs that exact revision.
        explicit_v1 = env.run_workflow(wf_id, revision_id=rev1, inputs={"text": "explicit-v1"}, timeout_s=180)
        explicit_v1_res = explicit_v1.get("result") or {}
        assert explicit_v1_res.get("status") == "completed", explicit_v1
        explicit_v1_row = client.get_workflow_run(explicit_v1_res["workflow_run_id"])
        assert explicit_v1_row.revision_id == rev1
        assert explicit_v1_res.get("outputs", {}).get("nd_output") == "explicit-v1"

    second = Session(api_key=env.poor_key(), backend_url=env.BACKEND)
    with second:
        # Second user runs with no revision_id -> must run published revision (rev1).
        stranger_run = env.run_workflow(wf_id, inputs={"text": "stranger"}, timeout_s=180)
        stranger_res = stranger_run.get("result") or {}
        assert stranger_res.get("status") == "completed", stranger_run
        stranger_row = client.get_workflow_run(stranger_res["workflow_run_id"])
        assert stranger_row.revision_id == rev1
        assert stranger_res.get("outputs", {}).get("nd_output") == "stranger"

        fetched = client.get_workflow(wf_id)
        assert fetched is not None, "second user cannot see the published workflow"
        document = fetched.document.model_dump(mode="json", exclude_none=True)
        env.log("T2B", f"second user fetched published workflow: {fetched.title}")

        # Saving a foreign public workflow forks the lineage into a new workflow owned by second user.
        modified = copy.deepcopy(document)
        modified.get("metadata", {}).pop("content_hash", None)
        modified["nodes"].append(
            {"id": "nd_note", "kind": "transform", "title": "Clean", "op": "remove_empty"}
        )
        forked = client.upsert_workflow(modified, message="python fork revision")
        assert forked is not None and forked.forked is True
        fork_id = forked.workflow.id
        assert fork_id != wf_id
        env.log("T2B", f"fork id={fork_id}")

        fork_revisions = client.query_workflow_revisions(fork_id)
        env.log("T2B", f"fork revisions: {[(r.id, r.message) for r in fork_revisions]}")
        fork_doc = client.get_workflow(fork_id).document
        env.log("T2B", f"fork nodes: {[n.id for n in fork_doc.nodes]}")

        fork_run = env.run_workflow(fork_id, inputs={"text": "hello"}, timeout_s=180)
        result = fork_run.get("result") or {}
        env.log("T2B", f"fork run job={fork_run['job_id']} status={fork_run['status']} run_status={result.get('status')}")
        assert result.get("status") == "completed", result

        # Revert to the fork's base revision (the copied original content).
        base_revision = fork_revisions[-1]
        reverted = client.revert_workflow(fork_id, revision_id=base_revision.id)
        assert reverted is not None, "revert failed"
        after = client.get_workflow(fork_id).document
        env.log("T2B", f"after revert nodes: {[n.id for n in after.nodes]}")
        original_ids = sorted(n["id"] for n in BASE_DOC["nodes"])
        assert sorted(n.id for n in after.nodes) == original_ids, "revert did not restore the original document"
    env.log("done", "PASS")


def test_publish_fork() -> None:
    run()


if __name__ == "__main__":
    run()
