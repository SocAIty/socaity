"""Minimalistic, high-signal E2E test for nested workflows + revision pinning + propagation opt-out.

Covers:
1. Child workflow revision 1 executes inside two parent workflows (`parent_a`, `parent_b`) and writes `nested_run_id` trace.
2. Child workflow updates to revision 2 with propagation to `parent_a` only (`parent_b` opted out).
3. Running `parent_a` executes child rev 2; running `parent_b` stays pinned to child rev 1.

    python test/test_e2e_nested_workflow.py
    pytest test/test_e2e_nested_workflow.py -v -s
"""
from __future__ import annotations

import copy
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


def _child_doc(wf_id: str, tag: str) -> dict:
    return {
        "id": wf_id,
        "title": f"Nested child {tag}",
        "goal": "Tag incoming text.",
        "nodes": [
            {"id": "nd_in", "kind": "transform", "title": "in", "op": "identity"},
            {"id": "nd_out", "kind": "transform", "title": "out", "op": "identity"},
        ],
        "edges": [
            {"id": "ed_1", "source": "nd_in", "target": "nd_out", "map": f"[`{tag}`, text]"},
        ],
    }


def _parent_doc(title: str, child_wf_id: str, child_rev_id: str) -> dict:
    return {
        "id": f"wf_{uuid4()}",
        "title": title,
        "goal": "Call nested child workflow.",
        "nodes": [
            {"id": "nd_in", "kind": "transform", "title": "in", "op": "identity"},
            {
                "id": "nd_nested",
                "kind": "workflow",
                "title": "child",
                "workflow_id": child_wf_id,
                "revision_id": child_rev_id,
            },
            {"id": "nd_out", "kind": "transform", "title": "out", "op": "identity"},
        ],
        "edges": [
            {"id": "ed_in_nested", "source": "nd_in", "target": "nd_nested"},
            {"id": "ed_nested_out", "source": "nd_nested", "target": "nd_out"},
        ],
    }


def run() -> None:
    ts = int(time.time())
    with Session(api_key=env.api_key(), backend_url=env.BACKEND):
        child_id = f"wf_{uuid4()}"
        c1 = client.upsert_workflow(_child_doc(child_id, "v1"), slug=f"nested-child-{ts}", message="child v1")
        rev1 = c1.revision.id
        assert c1.workflow.contract is not None and c1.workflow.contract.specification == "workflow"
        assert [p.name for p in c1.workflow.contract.endpoints[0].parameters] == ["text"]

        p_a = client.upsert_workflow(
            _parent_doc(f"Parent A {ts}", c1.workflow.id, rev1),
            slug=f"nested-parent-a-{ts}",
            message="parent a",
        )
        assert p_a.workflow.contract is not None
        assert [p.name for p in p_a.workflow.contract.endpoints[0].parameters] == ["text"]
        p_b = client.upsert_workflow(
            _parent_doc(f"Parent B {ts}", c1.workflow.id, rev1),
            slug=f"nested-parent-b-{ts}",
            message="parent b",
        )

        # Verify dependents discovery lists both parents.
        dependents = client.get_workflow_dependents(c1.workflow.id)
        dep_ids = {d["id"] for d in dependents}
        assert p_a.workflow.id in dep_ids and p_b.workflow.id in dep_ids, dep_ids

        # Execute Parent A on child v1 and assert nested_run_id trace.
        run_a1 = env.run_workflow(p_a.workflow.id, inputs={"text": "alpha"}, timeout_s=180)
        res_a1 = run_a1.get("result") or {}
        assert res_a1.get("status") == "completed", run_a1
        assert res_a1.get("outputs", {}).get("nd_out") == ["v1", "alpha"]

        run_row_a1 = client.get_workflow_run(res_a1["workflow_run_id"], expand=["traces"])
        nested_trace = next((t for t in (run_row_a1.traces or []) if t.node_id == "nd_nested"), None)
        assert nested_trace is not None and nested_trace.nested_run_id, run_row_a1.traces
        child_run_row = client.get_workflow_run(nested_trace.nested_run_id)
        assert child_run_row.revision_id == rev1

        # Save child v2, propagating ONLY to Parent A (opting out Parent B).
        c2_doc = copy.deepcopy(_child_doc(c1.workflow.id, "v2"))
        c2 = client.upsert_workflow(
            c2_doc,
            message="child v2",
            propagate_to_workflow_ids=[p_a.workflow.id],
        )
        rev2 = c2.revision.id
        assert rev2 != rev1
        assert c2.propagated_workflow_ids == [p_a.workflow.id]

        # Parent A now runs child v2; Parent B stays pinned to child v1.
        run_a2 = env.run_workflow(p_a.workflow.id, inputs={"text": "beta"}, timeout_s=180)
        res_a2 = run_a2.get("result") or {}
        assert res_a2.get("status") == "completed", run_a2
        assert res_a2.get("outputs", {}).get("nd_out") == ["v2", "beta"]

        run_b = env.run_workflow(p_b.workflow.id, inputs={"text": "beta"}, timeout_s=180)
        res_b = run_b.get("result") or {}
        assert res_b.get("status") == "completed", run_b
        assert res_b.get("outputs", {}).get("nd_out") == ["v1", "beta"]

        # Multi-output `is_output: True` on intermediate node exposes both in contract and run outputs.
        multi_doc = copy.deepcopy(client.get_workflow(p_a.workflow.id).document.model_dump(mode="json", exclude_none=True))
        multi_doc.get("metadata", {}).pop("content_hash", None)
        next(n for n in multi_doc["nodes"] if n["id"] == "nd_in")["is_output"] = True
        p_multi = client.upsert_workflow(multi_doc, message="expose intermediate output")
        multi_schema = p_multi.workflow.contract.endpoints[0].responses["200"]["content"]["application/json"]["schema"]
        assert set(multi_schema.get("properties", {}).keys()) == {"nd_in", "nd_out"}
        multi_run = env.run_workflow(p_multi.workflow.id, inputs={"text": "dual"}, timeout_s=180)
        multi_res = multi_run.get("result") or {}
        assert multi_res.get("status") == "completed", multi_run
        assert multi_res.get("outputs") == {"nd_in": {"text": "dual"}, "nd_out": ["v2", "dual"]}, multi_res
        env.log("nested", "PASS")


def test_nested_workflow() -> None:
    run()


if __name__ == "__main__":
    run()
