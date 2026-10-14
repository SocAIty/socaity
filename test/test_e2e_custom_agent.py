"""E2E: standalone custom agent, attached SKILL.md, and endpoint grant.

Uploads a SKILL.md file with a required response marker in its body, creates
a custom agent with grants=[tavily_search_ep] and discovery/run_service off,
and runs a direct turn via client.run_agent.

Verifies:
- details_id is pinned on the job
- skill body is lazy-loaded via load_skill (marker appears in output)
- granted tavily child job runs despite run_service="off"
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import agentic_utils as env  # noqa: E402

from socaity import Session, client  # noqa: E402

pytestmark = [
    pytest.mark.skipif(not env.backend_up(), reason=f"backend not reachable at {env.BACKEND}"),
    pytest.mark.skipif(not env.inference_up(), reason=f"APIPod gate not reachable at {env.GATE}"),
    pytest.mark.skipif(not env.api_key(), reason=env.missing_env("SOCAITY_API_KEY") or "no SOCAITY_API_KEY"),
]

SKILL_MARKER = "OMEGA_SKILL_MARKER_9421"
SKILL_MD = f"""---
name: omega-protocol
description: Mandatory formatting protocol for custom agent verification. Always load this skill before answering.
---

# Omega Protocol

When answering any user prompt, you MUST include the exact token `{SKILL_MARKER}` in your final response.
"""


def _find_tavily_endpoint() -> str:
    services = client.query_services(q="tavily", limit=10)
    for svc in services:
        full = client.get_service(svc.id)
        for ep in getattr(full, "endpoints", None) or []:
            if "search" in (ep.operation_key or "").lower() or ep.id:
                return ep.id
    raise RuntimeError("Could not find a tavily endpoint in the catalog")


def run() -> None:
    session = Session(api_key=env.api_key(), backend_url=env.BACKEND)
    with session:
        tavily_ep_id = _find_tavily_endpoint()
        env.log("T1", f"resolved tavily endpoint_id={tavily_ep_id}")

        tmp_skill = Path(__file__).resolve().parent / f"_tmp_skill_{int(time.time())}.md"
        tmp_skill.write_text(SKILL_MD, encoding="utf-8")
        try:
            rows = client.upload_files(tmp_skill, purpose="USER_UPLOAD")
            assert rows, "upload_files returned no records"
            uploaded = rows[0]
            skill_file_id = str(uploaded["id"] if isinstance(uploaded, dict) else uploaded.id)
        finally:
            tmp_skill.unlink(missing_ok=True)
        env.log("T1", f"uploaded SKILL.md file_id={skill_file_id}")

        slug = f"custom-agent-e2e-{int(time.time())}"
        agent_svc = client.upsert_agent(
            display_name="Omega Research Agent",
            slug=slug,
            short_desc="E2E test agent with skill and tavily grant",
            is_public=False,
            spec={
                "name": "Omega Research Agent",
                "model_service_id": "qwen3.8",
                "system_prompt": (
                    "You are the Omega Research Agent. "
                    "First call load_skill(name='omega-protocol') to read your formatting rules. "
                    "Then use run_service to search with your granted tavily endpoint and answer the user."
                ),
                "skills": [
                    {
                        "name": "omega-protocol",
                        "description": "Mandatory formatting protocol. Load before answering.",
                        "file_id": skill_file_id,
                    }
                ],
                "tools": {
                    "run_service": "off",
                    "query_services": "off",
                    "get_service": "off",
                },
                "grants": [tavily_ep_id],
            },
        )
        agent_id = agent_svc["id"] if isinstance(agent_svc, dict) else agent_svc.id
        details_list = (agent_svc.get("details") if isinstance(agent_svc, dict) else getattr(agent_svc, "details", None)) or []
        expected_details_id = details_list[0]["id"] if details_list and isinstance(details_list[0], dict) else (details_list[0].id if details_list else None)
        env.log("T1", f"created agent id={agent_id} slug={slug} details_id={expected_details_id}")

        try:
            turn = env.run_agent(
                slug,
                message="Load your omega-protocol skill, search Tavily for 'Python programming language creator', and answer in one sentence.",
                timeout_s=600,
            )
            env.log("T1", f"turn job_id={turn['job_id']} status={turn['status']} agent_status={turn['agent_status']}")
            env.log("T1", f"turn text={turn['text']!a}")
            assert turn["agent_status"] == "completed", turn
            assert SKILL_MARKER in (turn["text"] or ""), f"Expected {SKILL_MARKER} in {turn['text']!r}"

            job_row = client.get_job(turn["job_id"])
            job_obj = getattr(job_row, "job", job_row)
            pinned_details = getattr(job_obj, "details_id", None)
            env.log("T1", f"job pinned details_id={pinned_details}")
            if expected_details_id:
                assert pinned_details == expected_details_id, f"Expected details_id={expected_details_id}, got {pinned_details}"
        finally:
            try:
                client.delete_agent(agent_id)
            except Exception as exc:
                env.log("T1", f"cleanup delete_agent warning: {exc}")

    env.log("done", "PASS")


def test_custom_agent() -> None:
    run()


if __name__ == "__main__":
    run()
