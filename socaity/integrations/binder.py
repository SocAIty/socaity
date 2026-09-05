"""Session-aware binder: inspect SDK methods, bind to the active client, serialize."""
from __future__ import annotations

import asyncio
import inspect
import queue
from contextlib import nullcontext
from typing import Any, Callable, Optional

from fastsdk.service_interaction.api_seex import APISeex, JobEvent

from socaity.integrations.policy import (
    DESTRUCTIVE_METHODS,
    RUN_METHODS,
    exposed_signature,
)
from socaity.core.serialize import agent_turn_from_job, serialize_job, serialize_value


def _session_scope(session):
    """Accept a Session, a session factory, or a context-manager factory."""
    if session is None:
        from socaity.core.session import current_session
        return nullcontext(current_session())
    acquired = session() if callable(session) else session
    if hasattr(acquired, "__enter__"):
        return acquired
    return nullcontext(acquired)


def _publish_runtime_event(event: JobEvent, tool_name: str) -> None:
    """LangGraph custom stream: tool start / progress / end / error."""
    try:
        from langgraph.config import get_stream_writer
        writer = get_stream_writer()
    except Exception:
        return
    if writer is None:
        return
    kind_map = {
        "started": "start",
        "progress": "progress",
        "finished": "end",
        "error": "error",
    }
    payload = {
        "object": "tool.lifecycle",
        "event": kind_map.get(event.kind, event.kind),
        "tool": tool_name,
        "job_id": event.job_id,
        "message": event.message,
        "progress": event.progress,
    }
    if event.kind == "error" and event.error is not None:
        payload["error"] = str(event.error)
    writer(payload)


def consume_job_sync(job: APISeex, tool_name: str) -> dict:
    """Wait for the terminal job event and return a JSON-serializable result."""
    events: queue.Queue = queue.Queue()

    def enqueue(event: JobEvent) -> None:
        events.put(event)

    unsubscribe = job.subscribe(
        on_started=enqueue,
        on_progress=enqueue,
        on_finished=enqueue,
        on_error=enqueue,
        replay=True,
    )
    try:
        while True:
            try:
                event = events.get(timeout=0.25)
            except queue.Empty:
                if job.is_terminal:
                    if job.error is not None:
                        raise job.error
                    result = serialize_job(job)
                    if tool_name == "run_agent":
                        return agent_turn_from_job(job)
                    return result
                continue
            _publish_runtime_event(event, tool_name)
            if event.kind == "finished":
                if tool_name == "run_agent":
                    return agent_turn_from_job(job)
                return serialize_job(job, event.result)
            if event.kind == "error":
                raise event.error or RuntimeError("Job failed")
    finally:
        unsubscribe()


def consume_or_serialize(method: Callable, result: Any) -> Any:
    if method in RUN_METHODS:
        return consume_job_sync(result, method.__name__)
    return serialize_value(result)


def bind_method(method: Callable, session: Optional[Callable] = None):
    """Bind an unbound client method to the active session and expose it without ``self``."""

    def invoke_sync(**arguments):
        with _session_scope(session) as active:
            result = method(active.client, **arguments)
            return consume_or_serialize(method, result)

    async def invoke_async(**arguments):
        return await asyncio.to_thread(invoke_sync, **arguments)

    signature = exposed_signature(method)
    doc = inspect.getdoc(method)
    annotations = {
        name: parameter.annotation
        for name, parameter in signature.parameters.items()
        if parameter.annotation is not inspect.Parameter.empty
    }
    if signature.return_annotation is not inspect.Signature.empty:
        annotations["return"] = signature.return_annotation
    for function in (invoke_sync, invoke_async):
        function.__name__ = method.__name__
        function.__doc__ = doc
        function.__module__ = method.__module__
        function.__signature__ = signature
        function.__annotations__ = annotations

    metadata = {
        "destructive": method in DESTRUCTIVE_METHODS,
        "execution": "job" if method in RUN_METHODS else "direct",
    }
    return invoke_sync, invoke_async, metadata
