"""Agent-first service invocation: ``service@/endpoint`` + JSON args."""
from __future__ import annotations

import time
from typing import Any, Dict, Optional, Tuple

from socaity.core.catalog import connect, get_service
from socaity.core.jobs import get_job
from socaity.integrations.mcp.auth import ensure_api_key
from socaity.integrations.mcp.serialize import to_jsonable


def parse_call(call: str) -> Tuple[str, str]:
    """Split ``service@/endpoint`` into ``(service, endpoint_path)``.

    Service ids/names may contain ``/`` (e.g. ``bytedance/sdxl-lightning-4step``).
    The last ``@`` separates service from endpoint. Endpoint may omit the leading
    slash; it is normalised to start with ``/``.

    Examples:
        bytedance/sdxl-lightning-4step@/predict
        qwen35@chat
        my-org/my-svc@/v1/generate
    """
    text = (call or "").strip()
    if not text or "@" not in text:
        raise ValueError(
            "call must look like 'service@/endpoint' "
            "(example: bytedance/sdxl-lightning-4step@/predict)"
        )
    service, endpoint = text.rsplit("@", 1)
    service = service.strip()
    endpoint = endpoint.strip()
    if not service or not endpoint:
        raise ValueError("call must include both service and endpoint around '@'")
    if not endpoint.startswith("/"):
        endpoint = "/" + endpoint
    return service, endpoint


def run_call(
    call: str,
    args: Optional[Dict[str, Any]] = None,
    *,
    wait: bool = True,
    timeout_s: float = 600.0,
) -> Dict[str, Any]:
    """Submit ``args`` to ``service@/endpoint``; optionally wait for completion.

    Results keep file URLs (``FASTSDK_MATERIALIZE_MEDIA=0``). Download with
    ``get_files`` when the agent needs bytes on disk.
    """
    ensure_api_key()
    service_ref, endpoint = parse_call(call)
    args = dict(args or {})

    svc = get_service(service_ref, expand=["endpoints", "deployments"])
    if svc is None:
        raise ValueError(f"Unknown service: {service_ref}")

    client = connect(svc, api_key=ensure_api_key())
    handle = client.submit_job(endpoint, **args)

    job_id = _wait_for_job_id(handle, timeout_s=min(timeout_s, 120.0))
    if not wait:
        return {
            "status": "submitted",
            "call": f"{service_ref}@{endpoint}",
            "job_id": job_id,
            "hint": "Poll with get_job(job_id) or re-run with wait=true.",
        }

    # Prefer platform job row (URLs in result) over SDK media materialization.
    if job_id:
        job = _poll_platform_job(job_id, timeout_s=timeout_s)
        return {
            "status": getattr(job, "status", None) if job else "unknown",
            "call": f"{service_ref}@{endpoint}",
            "job_id": job_id,
            "job": to_jsonable(job),
            "files": to_jsonable(getattr(job, "files", None) or []),
        }

    raw = handle.wait_for_result(timeout_s=timeout_s)
    return {
        "status": "finished",
        "call": f"{service_ref}@{endpoint}",
        "job_id": job_id,
        "result": to_jsonable(raw),
    }


def _wait_for_job_id(handle: Any, timeout_s: float) -> Optional[str]:
    deadline = time.time() + max(timeout_s, 1.0)
    while time.time() < deadline:
        resp = getattr(handle, "response", None)
        if resp is not None:
            job_id = getattr(resp, "id", None) or getattr(resp, "job_id", None)
            if job_id:
                return str(job_id)
        time.sleep(0.25)
    return None


def _poll_platform_job(job_id: str, timeout_s: float) -> Any:
    deadline = time.time() + max(timeout_s, 1.0)
    terminal = {"finished", "failed", "cancelled", "canceled", "error", "completed", "success"}
    last = None
    while time.time() < deadline:
        last = get_job(job_id, expand=["data", "files"])
        status = (getattr(last, "status", None) or "").lower() if last else ""
        if status in terminal:
            return last
        time.sleep(1.0)
    return last
