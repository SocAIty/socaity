"""E2E: broken workflow (missing field) repaired through the full stack.

Save the broken document, run it via the gateway. Expect: mapper exhausts,
planner (live SPAINE) repairs with HIT -> run interrupted + repaired revision
persisted. Re-run the workflow (latest revision) -> completed.

    python test/test_e2e_workflow_repair.py
    pytest test/test_e2e_workflow_repair.py -v -s

Needs socaity_backend (:8000) + inference stack (:8001) + the sibling
``socaity-workflows`` checkout. Keys: see ``agentic_utils``.
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

import socaity  # noqa: E402
from socaity.core.session import Session, use_session  # noqa: E402

DOC_FILE = env.PROJECTS_ROOT / "socaity-workflows" / "tests" / "workflows" / "missing_field.json"
INPUTS = {"text": "hello"}

pytestmark = [
    pytest.mark.skipif(not env.backend_up(), reason=f"backend not reachable at {env.BACKEND}"),
    pytest.mark.skipif(not env.inference_up(), reason=f"APIPod gate not reachable at {env.GATE}"),
    pytest.mark.skipif(not env.rich_key(), reason="no test API key (SOCAITY_TEST_RICH_KEY / SOCAITY_API_KEY)"),
    pytest.mark.skipif(not DOC_FILE.is_file(), reason=f"missing workflow fixture {DOC_FILE}"),
]


def run() -> None:
    document = json.loads(DOC_FILE.read_text())
    document["id"] = f"wf_{uuid4()}"
    slug = f"missing-field-{int(time.time())}"

    session = Session(api_key=env.rich_key(), backend_url=env.BACKEND)
    with use_session(session):
        saved = env.sdk().upsert_workflow(document, slug=slug, message="workflow repair e2e broken doc")
        assert saved and saved.workflow, "workflow upsert failed"
        wf_id = saved.workflow.id
        env.log("T1", f"saved workflow id={wf_id} slug={slug} revision={saved.revision.id if saved.revision else None}")

        run1 = env.run_workflow(wf_id, inputs=INPUTS, timeout_s=900)
        result1 = run1.get("result") or {}
        env.log("T1", f"run1 job={run1['job_id']} status={run1['status']} run_status={result1.get('status')}")
        env.log("T1", f"run1 result={json.dumps(result1, default=str)[:600]}")
        assert run1["status"] == "finished", run1
        assert result1.get("status") in ("interrupted", "completed"), result1

        revisions = env.sdk().query_workflow_revisions(wf_id)
        env.log("T1", f"revisions after run1: {len(revisions)} -> {[(r.version, r.message) for r in revisions]}")

        if result1.get("status") == "interrupted":
            assert len(revisions) >= 2, "HIT pause must persist the repaired revision"
            run2 = env.run_workflow(wf_id, inputs=INPUTS, timeout_s=900)
            result2 = run2.get("result") or {}
            env.log("T1", f"run2 job={run2['job_id']} status={run2['status']} run_status={result2.get('status')}")
            env.log("T1", f"run2 outputs={json.dumps(result2.get('outputs'), default=str)[:400]}")
            assert run2["status"] == "finished", run2
            assert result2.get("status") == "completed", result2
        else:
            env.log("T1", "planner completed without HIT pause (allowed); checking repair revision")
            assert len(revisions) >= 2, "repair must persist a new revision"
            env.log("T1", f"outputs={json.dumps(result1.get('outputs'), default=str)[:400]}")

        runs = env.sdk().query_workflow_runs(wf_id)
        env.log("T1", f"runs recorded: {[(r.id, r.status) for r in runs]}")
    env.log("done", "PASS")


def test_workflow_repair() -> None:
    run()


if __name__ == "__main__":
    run()
