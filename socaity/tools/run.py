"""Execution tools: run a service endpoint and estimate what it will cost."""

from __future__ import annotations

import time
from typing import Any, Callable, Dict, List, Optional

from fastsdk import APISeex, FastClient
from fastsdk.service_access import service_contract

from socaity.core.catalog import connect

DEFAULT_JOB_TIMEOUT_S = 1800.0
DEFAULT_POLL_INTERVAL_S = 1.0


def _resolve_endpoint(client: FastClient, endpoint: Optional[str]):
    """Pick the requested endpoint, or the service's first one when none was named."""
    endpoints = service_contract(client.service).endpoints
    if not endpoints:
        raise ValueError(f"Service '{client.service.name or client.service.id}' exposes no endpoints.")
    if endpoint is None:
        return endpoints[0]

    wanted = endpoint if endpoint.startswith("/") else f"/{endpoint}"
    for candidate in endpoints:
        if candidate.path == wanted:
            return candidate
    known = ", ".join(candidate.path for candidate in endpoints)
    raise ValueError(f"Endpoint '{endpoint}' not found. This service exposes: {known}")


def _call_params(endpoint, params: Optional[dict], flags: Dict[str, Any]) -> dict:
    """Merge caller params with the job flags the endpoint actually accepts."""
    call = dict(params or {})
    accepted = {parameter.name for parameter in endpoint.parameters}
    call.update({name: value for name, value in flags.items() if name in accepted})
    return call


def _collect_urls(value: Any, urls: List[str]) -> None:
    if isinstance(value, dict):
        url = value.get("url")
        if isinstance(url, str) and url.startswith("http"):
            urls.append(url)
        for nested in value.values():
            _collect_urls(nested, urls)
    elif isinstance(value, list):
        for item in value:
            _collect_urls(item, urls)


def platform_job_id(job: APISeex) -> Optional[str]:
    """Platform job id of a submitted fastsdk job, once the gateway assigned one."""
    response = job.response
    return getattr(response, "job_id", None) or getattr(response, "id", None)


def job_payload(job: APISeex, job_id: Optional[str], status: str) -> dict:
    """Uniform result envelope of ``run_service``."""
    urls: List[str] = []
    result = job.result if status == "finished" else None
    _collect_urls(result, urls)
    delay_s, execution_s = job.runtime_info
    return {
        "job_id": job_id,
        "status": status,
        "result": result,
        "files": urls,
        "queue_time_s": delay_s,
        "execution_time_s": execution_s,
    }


def run_service(
    service: str,
    endpoint: Optional[str] = None,
    params: Optional[dict] = None,
    is_public: bool = False,
    expires_at: Optional[str] = None,
    timeout_s: Optional[float] = None,
    poll_interval_s: float = DEFAULT_POLL_INTERVAL_S,
    on_progress: Optional[Callable[[float, str], None]] = None,
    on_job_start: Optional[Callable[[str, APISeex], None]] = None,
) -> dict:
    """Run an AI service and wait for its result. This is how work gets done here.

    Call get_service (with ``expand`` including ``deployments.contract``) or
    query_services with the same expand when you do not know the parameter names:
    ``params`` keys must match that endpoint's parameters exactly.

    File results come back as URLs, never as bytes. Hand those URLs to the user or
    download them yourself; the platform deliberately does not move the data twice.

    Args:
        service: Service id, name, "owner/service" or model slug, as returned by
            query_services. The service is resolved through the catalog.
        endpoint: Endpoint path such as "/predictions". Defaults to the service's
            first endpoint, which is the right one for single-purpose services.
        params: Endpoint arguments, e.g. {"prompt": "a cute robot dog"}.
        is_public: Publish the job and its results in the socaity feed. Default private.
        expires_at: Optional ISO timestamp for produced files. Null keeps them permanently.
        timeout_s: Give up waiting after this many seconds. The job keeps running on
            the platform; poll it with get_job.
        poll_interval_s: Delay between progress samples of the running job.
        on_progress: Called with (progress 0..1, message) whenever progress changes.
        on_job_start: Called once with (platform job id, fastsdk job handle) as soon
            as the gateway assigned an id. Hosts use it to register live jobs.

    Returns:
        job_id, status, result, and a ``files`` list of result URLs. On timeout the
        status is "running" and the job_id is still valid for get_job. Failed jobs
        include ``error``.
    """
    deadline = time.monotonic() + (timeout_s or DEFAULT_JOB_TIMEOUT_S)
    job_id: Optional[str] = None

    client = connect(service)
    target = _resolve_endpoint(client, endpoint)
    job = client.submit_job(
        target.path,
        **_call_params(target, params, {"is_public": is_public, "expires_at": expires_at}),
    )

    reported = -1.0
    while not job.is_terminal:
        if job_id is None:
            job_id = platform_job_id(job)
            if job_id and on_job_start:
                on_job_start(job_id, job)

        if on_progress and job.progress != reported:
            reported = job.progress
            message = job.task_progress.message if job.task_progress else str(job.task)
            on_progress(reported, message)

        if time.monotonic() > deadline:
            return job_payload(job, job_id, "running")

        time.sleep(poll_interval_s)

    job_id = job_id or platform_job_id(job)
    if job.error is not None:
        payload = job_payload(job, job_id, "failed")
        payload["error"] = str(job.error)
        return payload

    if on_progress:
        on_progress(1.0, "finished")
    return job_payload(job, job_id, "finished")


def estimate_price(
    service: str,
    endpoint: Optional[str] = None,
    params: Optional[dict] = None,
) -> dict:
    """Estimate price and runtime of a job before running it.

    Use this when the user asks what something costs, or before a batch that would be
    expensive to get wrong. Estimates are based on historical runs of the endpoint,
    so they are indicative rather than a quote.

    Args:
        service: Service id, name or "owner/service".
        endpoint: Endpoint path. Defaults to the service's first endpoint.
        params: The arguments you intend to pass to run_service. Input size moves the
            estimate, so pass the real ones.

    Returns:
        Estimated cost, currency and runtime for the endpoint.
    """
    client = connect(service)
    target = _resolve_endpoint(client, endpoint)
    estimate = client.estimate(target.path, **(params or {}))
    if estimate is None:
        raise ValueError(f"No estimate available for {service}{target.path}.")
    return estimate.model_dump(mode="json")
