"""E2E: create a flux-schnell job, refresh jobs catalog, search it via SDK.

Requires a running backend with Typesense, valid credentials
(SOCAITY_API_KEY or socaity login), and inference access.

    pytest test/test_e2e_jobs.py -v
"""
import json
import os
import time
import uuid
from pathlib import Path

import httpx
import pytest


def _load_repo_env() -> None:
    env_file = Path(__file__).resolve().parents[1] / ".env"
    if not env_file.is_file():
        return
    for line in env_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, _, value = line.partition("=")
            os.environ.setdefault(key.strip(), value.strip().strip('"'))


_load_repo_env()
os.environ.setdefault("SOCAITY_BACKEND_URL", "http://127.0.0.1:8000/")

import socaity  # noqa: E402
import socaity.core.catalog as catalog_mod  # noqa: E402

# Rebuild the backend client after env load (module import order / prior tests).
catalog_mod._client = None

BACKEND = os.environ["SOCAITY_BACKEND_URL"].rstrip("/") + "/"
PROMPT_TOKEN = f"e2e-jobs-{uuid.uuid4().hex[:10]}"
PROMPT = f"a lighthouse on a cliff at sunset, watercolor, {PROMPT_TOKEN}"


def _has_credentials() -> bool:
    if os.getenv("SOCAITY_API_KEY"):
        return True
    return (Path.home() / ".config" / "socaity" / "credentials.json").is_file()


def _backend_up() -> bool:
    try:
        return httpx.get(BACKEND + "v1/catalog/services", params={"limit": 1}, timeout=10).status_code == 200
    except httpx.HTTPError:
        return False


pytestmark = [
    pytest.mark.skipif(not _backend_up(), reason=f"backend not reachable at {BACKEND}"),
    pytest.mark.skipif(not _has_credentials(), reason="no credentials for inference / jobs"),
]


def _platform_job_id(handle) -> str:
    """Resolve the platform job UUID from an APISeex / response payload."""
    resp = getattr(handle, "response", None)
    for candidate in (
        getattr(resp, "job_id", None),
        getattr(resp, "id", None),
        getattr(handle, "job_id", None),
    ):
        if candidate:
            return str(candidate)
    raise AssertionError(f"could not resolve platform job id from handle={type(handle)} response={resp!r}")


@pytest.fixture(scope="module")
def created_job_id() -> str:
    client = socaity.connect("black-forest-labs-flux-schnell")
    handle = client.submit_job("/predictions", prompt=PROMPT)
    result = handle.get_result()
    assert result is not None, "flux-schnell returned no result"

    job_id = _platform_job_id(handle)

    # Inference writes the row; webhook loads it into JobCache + Typesense.
    deadline = time.time() + 180
    row = None
    while time.time() < deadline:
        refreshed = socaity.refresh_job(job_id)
        if not refreshed or refreshed.get("status") != "ok":
            time.sleep(2)
            continue
        row = socaity.get_job(job_id, expand=["data"])
        if row and (row.status or "").upper() == "FINISHED" and row.data:
            break
        time.sleep(2)
    else:
        pytest.fail(
            f"job {job_id} did not become FINISHED with data in time "
            f"(last_row={row!r}, hint: check SOCAITY_API_KEY owns the job)"
        )

    return job_id


def test_query_jobs_returns_visible_jobs(created_job_id):
    jobs = socaity.query_jobs(limit=20, expand=["data"])
    assert jobs, "query_jobs returned no jobs for the authenticated user"
    assert any(job.id == created_job_id for job in jobs), [job.id for job in jobs[:10]]


def test_get_job_by_id(created_job_id):
    job = socaity.get_job(created_job_id, expand=["data"])
    assert job is not None
    assert job.id == created_job_id
    assert job.data and job.data.input_data
    blob = json.dumps(job.data.input_data).lower()
    assert PROMPT_TOKEN.lower() in blob


def test_search_jobs_by_prompt_keyword(created_job_id):
    hits = socaity.query_jobs(q=PROMPT_TOKEN, limit=10)
    ids = [job.id for job in hits]
    assert created_job_id in ids, ids


def test_query_jobs_by_q(created_job_id):
    hits = socaity.query_jobs(q="lighthouse watercolor", expand=["data"], limit=20)
    ids = [job.id for job in hits]
    assert created_job_id in ids, ids


def test_webhook_refresh_indexes_job(created_job_id):
    again = socaity.refresh_job(created_job_id)
    assert again and again.get("job_id") == created_job_id
    assert again.get("indexed") is True
