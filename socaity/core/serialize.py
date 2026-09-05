"""JSON serialization of SDK values and FastSDK job handles."""
from __future__ import annotations

from typing import Any, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from fastsdk.service_interaction.api_seex import APISeex


def serialize_value(value: Any) -> Any:
    """JSON-ready view of a catalog entity, schema model, or backend dict."""
    if value is None:
        return None
    if hasattr(value, "model_dump"):
        return value.model_dump(mode="json", exclude_none=True)
    if isinstance(value, list):
        return [serialize_value(item) for item in value]
    if isinstance(value, dict):
        return {key: serialize_value(item) for key, item in value.items()}
    return value


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


def platform_job_id(job: "APISeex") -> Optional[str]:
    """Platform job id of a FastSDK handle, once the gateway assigned one."""
    return getattr(job, "platform_job_id", None) or _id_from_response(job.response)


def _id_from_response(response) -> Optional[str]:
    if response is None:
        return None
    return getattr(response, "job_id", None) or getattr(response, "id", None)


def serialize_job(job: "APISeex", result: Any = None) -> dict:
    """Uniform result envelope of a finished (or failed) FastSDK job."""
    job_id = platform_job_id(job)
    if job.error is not None:
        payload = {
            "job_id": job_id,
            "status": "failed",
            "result": None,
            "files": [],
            "error": str(job.error),
        }
        delay_s, execution_s = job.runtime_info
        payload["queue_time_s"] = delay_s
        payload["execution_time_s"] = execution_s
        return payload

    status = "finished"
    if job.termination_state is not None:
        name = getattr(job.termination_state, "name", "") or str(job.termination_state)
        if name == "CANCELLED":
            status = "cancelled"
    dumped_result = serialize_value(result if result is not None else job.result)
    urls: List[str] = []
    _collect_urls(dumped_result, urls)
    delay_s, execution_s = job.runtime_info
    return {
        "job_id": job_id,
        "status": status,
        "result": dumped_result,
        "files": urls,
        "queue_time_s": delay_s,
        "execution_time_s": execution_s,
    }


def agent_turn_from_job(job: "APISeex") -> dict:
    """Agent-turn envelope from a finished ``run_agent`` handle."""
    envelope = serialize_job(job)
    response = envelope.get("result") if isinstance(envelope.get("result"), dict) else {}
    if "choices" not in response and isinstance(response.get("output"), dict):
        response = response["output"]
    choices = response.get("choices") or []
    text = (choices[0].get("message") or {}).get("content") if choices else None
    return {
        "job_id": envelope.get("job_id"),
        "status": envelope.get("status"),
        "agent_status": response.get("status"),
        "thread_id": response.get("thread_id"),
        "text": text,
        "pending_actions": response.get("pending_actions") or [],
        "workflow": response.get("workflow"),
        "response": response,
    }
