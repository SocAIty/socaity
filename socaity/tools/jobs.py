"""Shared gateway submit/poll for first-party jobs (workflows, agents).

Catalog service jobs stay on FastSDK (``run_service``). Workflow runs and
agent turns post to gateway factories and poll ``GET /status/{job_id}``.
"""

from __future__ import annotations

import time
from typing import Any, Callable, Dict, Optional

import httpx

from socaity.core.session import current_session

DEFAULT_JOB_TIMEOUT_S = 1800.0
DEFAULT_POLL_INTERVAL_S = 1.0
TERMINAL_STATUSES = frozenset({"finished", "failed", "timeout", "cancelled", "rejected"})
_ERROR_STATUSES = frozenset({"failed", "timeout", "rejected"})


def _api_key() -> str:
    api_key = current_session().backend.api_key
    if not api_key:
        raise ValueError("No API key. Run `socaity login` or set SOCAITY_API_KEY.")
    return api_key


def gate_origin() -> str:
    """APIPod gate origin from the active session (``APIPOD_GATE_URL``)."""
    return current_session().gate_url


def poll_url(origin: str, envelope: dict, job_id: str) -> str:
    """Absolute status link from the envelope when present, else the standard route."""
    links = envelope.get("links") or {}
    status_link = links.get("status") if isinstance(links, dict) else None
    if isinstance(status_link, str) and status_link.startswith("http"):
        return status_link
    return f"{origin}/status/{job_id}"


def cancel_job_run(job_id: str, action: str = "cancel") -> dict:
    """Stop a running gateway job (``POST /cancel/{job_id}?action=...``).

    Args:
        job_id: Platform job id from a submit envelope.
        action: ``cancel`` (default, user stop: child jobs cancelled) or
            ``interrupt`` (HIT: child jobs keep running, resumable checkpoint).

    Returns:
        The gateway cancel summary.

    Raises:
        RuntimeError: Non-2xx cancel response.
        ValueError: No API key in the active session.
    """
    response = httpx.post(
        f"{gate_origin()}/cancel/{job_id}",
        params={"action": action},
        headers={"x-api-key": _api_key()},
        timeout=60,
    )
    if response.status_code not in (200, 202):
        raise RuntimeError(f"Job cancel failed ({response.status_code}): {response.text[:300]}")
    return response.json() if response.content else {}


def wait_for_job(
    job_id: str,
    *,
    timeout_s: Optional[float] = None,
    poll_interval_s: float = DEFAULT_POLL_INTERVAL_S,
) -> dict:
    """Wait on a running gateway job until it is terminal.

    Args:
        job_id: Platform job id from a submit envelope.
        timeout_s: Give up waiting after this many seconds (job keeps running).
        poll_interval_s: Delay between status polls.

    Returns:
        Status envelope with ``job_id``. On timeout the status is ``running``.
        ``cancelled`` is a normal terminal (not an error).

    Raises:
        RuntimeError: The job reached a terminal error state.
        ValueError: No API key in the active session.
    """
    origin = gate_origin()
    headers = {"x-api-key": _api_key()}
    deadline = time.monotonic() + (timeout_s or DEFAULT_JOB_TIMEOUT_S)
    status_url = f"{origin}/status/{job_id}"
    envelope: Dict[str, Any] = {"job_id": job_id, "status": "queued"}

    with httpx.Client(headers=headers, timeout=60) as client:
        while True:
            poll = client.get(status_url)
            if poll.status_code == 200:
                envelope = poll.json()
                status_url = poll_url(origin, envelope, job_id)
            status = (envelope.get("status") or "").lower()
            if status in TERMINAL_STATUSES:
                break
            if time.monotonic() > deadline:
                return {**envelope, "job_id": job_id, "status": "running"}
            time.sleep(poll_interval_s)

    status = (envelope.get("status") or "").lower()
    if envelope.get("error") or status in _ERROR_STATUSES:
        raise RuntimeError(f"Job failed: {envelope.get('error') or status}")
    return {**envelope, "job_id": job_id}


def interrupt_job(
    job_id: str,
    *,
    timeout_s: Optional[float] = None,
    poll_interval_s: float = DEFAULT_POLL_INTERVAL_S,
) -> dict:
    """Graceful stop (``action=interrupt``) then wait until the job is terminal.

    Checkpoint stays. Call before a follow-up ``run_agent`` on the same thread
    so ``begin_turn`` sees one leaf.

    Args:
        job_id: Live agent (or other gateway) job to stop.
        timeout_s: Give up waiting after this many seconds (job keeps running).
        poll_interval_s: Delay between status polls.

    Returns:
        Terminal status envelope. ``cancelled`` is success for this path.

    Raises:
        RuntimeError: Cancel failed, or the job errored / did not stop in time.
        ValueError: No API key in the active session.
    """
    cancel_job_run(job_id, action="interrupt")
    envelope = wait_for_job(job_id, timeout_s=timeout_s, poll_interval_s=poll_interval_s)
    status = (envelope.get("status") or "").lower()
    if status not in TERMINAL_STATUSES:
        raise RuntimeError(f"Previous turn did not stop in time | job_id={job_id} status={status}")
    return envelope


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
        path: Path under the gate origin, e.g. ``/v1/workflows/{id}/run``.
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
    origin = gate_origin()
    headers = {"x-api-key": _api_key()}
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
                status_url = poll_url(origin, envelope, job_id)

    status = (envelope.get("status") or "").lower()
    if envelope.get("error") or status in _ERROR_STATUSES:
        raise RuntimeError(f"Job failed: {envelope.get('error') or status}")

    if on_progress:
        on_progress(1.0, "finished")
    return {**envelope, "job_id": job_id}
