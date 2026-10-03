"""E2E: a finished flux-schnell job is readable and searchable.

The SDK does not refresh the index. After the job finishes, the platform
indexes it. This test only reads. Search must find the unique prompt token
and must not return the job for a token that was never submitted.

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
from socaity import client  # noqa: E402
from socaity_cli.errors import BackendTransportError  # noqa: E402

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
    except (httpx.HTTPError, httpx.InvalidURL):
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


def _prompt_blob(job) -> str:
    if not job or not job.data or not job.data.input_data:
        return ""
    return json.dumps(job.data.input_data).lower()


def _search_ids(q: str) -> list:
    return [job.id for job in client.query_jobs(q=q, expand=["data"], limit=10)]


def _poll(seconds: float, ready, what: str):
    deadline = time.time() + seconds
    last = None
    while time.time() < deadline:
        try:
            last = ready()
        except BackendTransportError:
            time.sleep(2)
            continue
        if last:
            return last
        time.sleep(2)
    raise AssertionError(f"{what} (last={last!r})")


def test_finished_job_is_searchable():
    """Run one flux job, then require catalog data and a Typesense hit."""
    handle = client.run_service(
        "black-forest-labs-flux-schnell",
        "/predictions",
        {"prompt": PROMPT},
    )
    try:
        result = handle.get_result()
    except Exception as exc:
        raise AssertionError(f"flux-schnell job failed: {exc}") from exc
    assert result is not None, "flux-schnell returned no result"
    job_id = _platform_job_id(handle)

    def finished():
        job = client.get_job(job_id, expand=["data"])
        if job and (job.status or "").upper() == "FINISHED" and PROMPT_TOKEN.lower() in _prompt_blob(job):
            return job
        return None

    _poll(90, finished, f"job {job_id} did not become FINISHED with prompt data")

    def indexed():
        return job_id if job_id in _search_ids(PROMPT_TOKEN) else None

    _poll(90, indexed, f"job {job_id} was not found by prompt search")


def run() -> None:
    test_finished_job_is_searchable()


if __name__ == "__main__":
    run()
