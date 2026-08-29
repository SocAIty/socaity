"""Shared gateway submit/poll for first-party jobs (workflows, agents).

Catalog service jobs stay on FastSDK (``execute_service``). Workflow runs and
agent turns post to gateway factories and poll ``GET /status/{job_id}``.
"""

from __future__ import annotations

import os
import time
from typing import Any, Callable, Dict, Optional

import httpx

from socaity.core.session import current_session

DEFAULT_JOB_TIMEOUT_S = 1800.0
DEFAULT_POLL_INTERVAL_S = 1.0
DEFAULT_INFERENCE_URL = "https://api.socaity.ai"
TERMINAL_STATUSES = frozenset({"finished", "failed", "timeout", "cancelled", "rejected"})


def inference_origin() -> str:
    """Gateway origin. Same env names as ``socaity_backend`` and the frontend."""
    for key in ("INFERENCE_BACKEND_URL", "NUXT_PUBLIC_INFER_API_BASE_URL", "SOCAITY_API_BASE"):
        value = (os.environ.get(key) or "").strip()
        if value:
            return value.rstrip("/")
    return DEFAULT_INFERENCE_URL


def poll_url(origin: str, envelope: dict, job_id: str) -> str:
    """Absolute status link from the envelope when present, else the standard route."""
    links = envelope.get("links") or {}
    status_link = links.get("status") if isinstance(links, dict) else None
    if isinstance(status_link, str) and status_link.startswith("http"):
        return status_link
    return f"{origin}/status/{job_id}"


def submit_and_poll(
    path: str,
    body: dict,
    *,
    timeout_s: Optional[float] = None,
    poll_interval_s: float = DEFAULT_POLL_INTERVAL_S,
    on_progress: Optional[Callable[[float, str], None]] = None,
    on_job_start: Optional[Callable[[str, Any], None]] = None,
    submit_error: str = "Job submit failed",
) -> dict:
    """POST a first-party gateway factory and poll until terminal.

    Args:
        path: Path under the inference origin, e.g. ``/v1/workflows/{id}/run``.
        body: JSON body. ``None`` values are dropped.
        timeout_s: Give up waiting after this many seconds (job keeps running).
        poll_interval_s: Delay between status polls.
        on_progress: Called with (progress 0..1, message) when progress changes.
        on_job_start: Called once with (job id, submit envelope).
        submit_error: Prefix for a non-2xx submit.

    Returns:
        Terminal job envelope with ``job_id``. On timeout the status is "running".

    Raises:
        RuntimeError: Submit failed or the job reached a terminal error state.
        ValueError: No API key in the active session.
    """
    api_key = current_session().backend.api_key
    if not api_key:
        raise ValueError("No API key. Run `socaity login` or set SOCAITY_API_KEY.")

    origin = inference_origin()
    headers = {"x-api-key": api_key}
    deadline = time.monotonic() + (timeout_s or DEFAULT_JOB_TIMEOUT_S)

    with httpx.Client(headers=headers, timeout=60) as client:
        response = client.post(
            f"{origin}{path}",
            json={key: value for key, value in body.items() if value is not None},
        )
        if response.status_code not in (200, 202):
            raise RuntimeError(f"{submit_error} ({response.status_code}): {response.text[:300]}")

        envelope: Dict[str, Any] = response.json()
        job_id = envelope.get("job_id")
        if not job_id:
            raise RuntimeError(f"Gateway returned no job id: {envelope}")
        if on_job_start:
            on_job_start(job_id, envelope)

        status_url = poll_url(origin, envelope, job_id)
        reported = -1.0
        while (envelope.get("status") or "").lower() not in TERMINAL_STATUSES:
            progress = envelope.get("progress")
            if on_progress and progress is not None and progress != reported:
                reported = float(progress)
                on_progress(reported, envelope.get("message") or str(envelope.get("status") or ""))

            if time.monotonic() > deadline:
                return {**envelope, "job_id": job_id, "status": "running"}

            time.sleep(poll_interval_s)
            poll = client.get(status_url)
            if poll.status_code == 200:
                envelope = poll.json()

    status = (envelope.get("status") or "").lower()
    if envelope.get("error") or status in ("failed", "timeout", "rejected"):
        raise RuntimeError(f"Job failed: {envelope.get('error') or status}")

    if on_progress:
        on_progress(1.0, "finished")
    return {**envelope, "job_id": job_id}
