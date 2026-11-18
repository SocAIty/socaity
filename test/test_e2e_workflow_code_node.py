"""E2E: Code (MiniRacer) + Transform (`op: "to_json"`) workflow execution.

Tests the 4 runtime invariants in `docs/planned/code_nodes/code-nodes.md`:
1. First Code service returns a markdown-fenced JSON string:
   `return "Result:\\n```json\\n{\\"left\\": 3, \\"right\\": 4}\\n```\\n";`
2. Transform node (`op: "to_json"`) parses the string into `{"left": 3, "right": 4}` in-process (0 child jobs).
3. Second Code service runs `return input.left + input.right;` and outputs `7` (asserting 2 child jobs total).
4. A Code service runs `return JSON.stringify({ raw: 42 });`. The worker parses that JSON string, so the
   stored job output is the object `{"raw": 42}` and the following `to_json` node sees the same object.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path
from uuid import uuid4

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import agentic_utils as env  # noqa: E402  (sets URL defaults before socaity import)

from apipod_registry import active_details  # noqa: E402
from socaity import Session, client  # noqa: E402

pytestmark = [
    pytest.mark.skipif(not env.backend_up(), reason=f"backend not reachable at {env.BACKEND}"),
    pytest.mark.skipif(not env.inference_up(), reason=f"APIPod gate not reachable at {env.GATE}"),
    pytest.mark.skipif(not env.api_key(), reason=env.missing_env("SOCAITY_API_KEY") or "no SOCAITY_API_KEY"),
]


def _resolve_miniracer():
    """Find the deployed MiniRacer Code service with `standard_schema == 'CodeExecuteRequest'`."""
    candidates = list(client.query_services(q="miniracer", limit=20) or [])
    candidates.extend(client.query_services(q="miniracer", mine=True, limit=20) or [])
    seen = set()
    expanded = []
    for row in candidates:
        if not row.id or row.id in seen:
            continue
        seen.add(row.id)
        svc = client.get_service(row.id, expand=["details.contract", "details.deployment", "endpoints"])
        if svc is not None:
            expanded.append(svc)

    for svc in expanded:
        details = active_details(svc)
        if not details or not details.contract:
            continue
        for ep in details.contract.endpoints or []:
            if ep.standard_schema == "CodeExecuteRequest":
                cat_ep = next((e for e in (svc.endpoints or []) if e.operation_key == ep.operation_key), None)
                return svc, details, ep, cat_ep

    raise AssertionError(
        "No deployed MiniRacer service with `standard_schema == 'CodeExecuteRequest'` found in catalog. "
        "Redeploy `qwen-models/miniracer_service` first."
    )


def _code_service_node(node_id: str, title: str, svc, details, ep, cat_ep, code: str) -> dict:
    return {
        "id": node_id,
        "kind": "service",
        "title": title,
        "service_id": svc.id,
        "endpoint_id": cat_ep.id if cat_ep else None,
        "operation_key": ep.operation_key,
        "details_id": details.id,
        "deployment_id": details.deployment.id if details.deployment else None,
        "specification_hash": details.specification_hash,
        "inputs": {"code": code},
    }


def run() -> None:
    session = Session(api_key=env.api_key(), backend_url=env.BACKEND)
    with session:
        svc, details, ep, cat_ep = _resolve_miniracer()
        env.log("CODE", f"resolved miniracer service_id={svc.id} details_id={details.id} schema={ep.standard_schema}")
        assert ep.standard_schema == "CodeExecuteRequest"

        # ── Part A: Pure JSON string preservation on direct job + workflow to_json ──
        direct_handle = client.run(
            f"{svc.id}/{ep.operation_key}",
            params={"code": "return JSON.stringify({ raw: 42 });"},
            details_id=details.id,
        )
        direct_out = direct_handle.get_result(timeout_s=180)
        env.log("CODE", f"direct JSON.stringify job={direct_handle.platform_job_id} type={type(direct_out).__name__} val={direct_out!r}")
        assert direct_out == {"raw": 42}, f"Expected parsed object from JSON.stringify, got {direct_out!r}"

        job_row = client.get_job(direct_handle.platform_job_id, expand=["data"])
        stored_out = job_row.data.output_data if job_row and job_row.data else None
        env.log("CODE", f"stored job_data.output_data type={type(stored_out).__name__} val={stored_out!r}")
        assert stored_out == {"raw": 42}, f"Expected stored object, got {stored_out!r}"

        # ── Part B: Code (fenced JSON) -> Transform (to_json) -> Code (sum) ──
        fenced_js = 'return "Result:\\n```json\\n{\\"left\\": 3, \\"right\\": 4}\\n```\\n";'
        sum_js = "return input.left + input.right;"
        wf_doc = {
            "id": f"wf_{uuid4()}",
            "title": "Code + Transform to_json E2E",
            "goal": "Emit fenced JSON from JS, decode with to_json transform, and sum in downstream JS.",
            "nodes": [
                _code_service_node("nd_emit", "Emit fenced JSON", svc, details, ep, cat_ep, fenced_js),
                {"id": "nd_parse", "kind": "transform", "title": "Convert", "op": "to_json", "config": {}},
                _code_service_node("nd_sum", "Sum fields", svc, details, ep, cat_ep, sum_js),
            ],
            "edges": [
                {"id": "ed_emit_parse", "source": "nd_emit", "target": "nd_parse"},
                {"id": "ed_parse_sum", "source": "nd_parse", "target": "nd_sum"},
            ],
        }

        saved = client.upsert_workflow(wf_doc, slug=f"code-transform-e2e-{int(time.time())}", message="e2e code + to_json")
        assert saved and saved.workflow, "workflow upsert failed"
        wf_id = saved.workflow.id
        env.log("CODE", f"saved workflow {wf_id}")

        wf_run = env.run_workflow(wf_id, inputs={}, timeout_s=300)
        env.log("CODE", f"workflow run status={wf_run.get('status')} result={json.dumps(wf_run.get('result'), default=str)}")
        assert wf_run.get("status") == "finished", wf_run
        result = wf_run.get("result") or {}
        assert result.get("status") == "completed", result
        outputs = result.get("outputs") or {}
        assert outputs.get("nd_sum") == 7, f"Expected output 7 on nd_sum, got {outputs}"

        # Verify exactly 2 child jobs (nd_emit + nd_sum) and 0 child jobs for Transform (nd_parse).
        runs = client.query_workflow_runs(wf_id)
        assert runs, "workflow run record missing"
        live_run = client.get_workflow_run(runs[0].id, expand=["traces"]) or runs[0]
        traces = live_run.traces or []
        child_job_traces = [t for t in traces if getattr(t, "job_id", None)]
        transform_traces = [t for t in traces if getattr(t, "node_id", None) == "nd_parse" and getattr(t, "job_id", None)]
        env.log("CODE", f"traces={[(t.node_id, t.kind, t.job_id) for t in traces]}")
        assert len(child_job_traces) == 2, f"Expected 2 billed child jobs, got {len(child_job_traces)}: {traces}"
        assert len(transform_traces) == 0, f"Transform node must not spawn a job: {transform_traces}"

        # Also verify raw JSON string preservation inside a workflow feeding into to_json:
        wf_raw_doc = {
            "id": f"wf_{uuid4()}",
            "title": "JSON.stringify parsed by the worker",
            "goal": "JSON.stringify is parsed by the worker; to_json passes the object through.",
            "nodes": [
                _code_service_node("nd_raw", "Stringify", svc, details, ep, cat_ep, "return JSON.stringify({ raw: 42 });"),
                {"id": "nd_to_json", "kind": "transform", "title": "Convert", "op": "to_json", "config": {}},
            ],
            "edges": [
                {"id": "ed_raw_json", "source": "nd_raw", "target": "nd_to_json"},
            ],
        }
        saved_raw = client.upsert_workflow(wf_raw_doc, slug=f"code-raw-json-e2e-{int(time.time())}", message="e2e raw json string")
        wf_raw_run = env.run_workflow(saved_raw.workflow.id, inputs={}, timeout_s=300)
        raw_res = wf_raw_run.get("result") or {}
        assert raw_res.get("status") == "completed", raw_res
        assert (raw_res.get("outputs") or {}).get("nd_to_json") == {"raw": 42}

        raw_runs = client.query_workflow_runs(saved_raw.workflow.id)
        raw_live = client.get_workflow_run(raw_runs[0].id, expand=["traces"]) or raw_runs[0]
        code_trace = next(t for t in (raw_live.traces or []) if t.node_id == "nd_raw")
        code_job = client.get_job(code_trace.job_id, expand=["data"])
        assert code_job.data.output_data == {"raw": 42}

    env.log("done", "PASS")


def test_e2e_workflow_code_node() -> None:
    run()


if __name__ == "__main__":
    run()
