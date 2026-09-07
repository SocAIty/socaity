"""Session-aware binder: inspect SDK methods, bind to the active client, serialize."""
from __future__ import annotations

import asyncio
import inspect
import queue
from contextlib import nullcontext
from typing import Any, Callable, Optional

from meseex import EventKind, MeseexEvent
from fastsdk.service_interaction.api_seex import APISeex

from socaity.integrations.policy import (
    DESTRUCTIVE_METHODS,
    RUN_METHODS,
    exposed_signature,
)
from socaity.core.serialize import agent_turn_from_job, serialize_job, serialize_value


def _session_scope(session):
    """Enter an optional Session, factory, or context-manager factory.

    ``None`` keeps the already-active session. MCP passes ``required_session``.
    """
    if session is None:
        return nullcontext()
    acquired = session() if callable(session) else session
    if hasattr(acquired, "__enter__"):
        return acquired
    return nullcontext()


_LIFECYCLE_KIND = {
    EventKind.STARTED: "start",
    EventKind.TASK_CHANGED: "progress",
    EventKind.PROGRESS: "progress",
    EventKind.SUCCEEDED: "end",
    EventKind.FAILED: "error",
    EventKind.CANCELLED: "end",
}


def _publish_runtime_event(event: MeseexEvent, tool_name: str, job: APISeex) -> None:
    """LangGraph custom stream: tool start / progress / end / error."""
    try:
        from langgraph.config import get_stream_writer
        writer = get_stream_writer()
    except Exception:
        return
    if writer is None:
        return
    message = event.message
    if event.kind is EventKind.TASK_CHANGED and event.task and not message:
        message = f"Task: {event.task}"
    payload = {
        "object": "tool.lifecycle",
        "event": _LIFECYCLE_KIND.get(event.kind, event.kind.value),
        "tool": tool_name,
        "job_id": job.platform_job_id,
        "message": message,
        "progress": event.task_progress if event.task_progress is not None else event.progress,
    }
    if event.kind is EventKind.FAILED and event.error is not None:
        payload["error"] = str(event.error)
    writer(payload)


def consume_job_sync(job: APISeex, tool_name: str) -> dict:
    """Wait for the terminal job event and return a JSON-serializable result."""
    events: queue.Queue = queue.Queue()

    def enqueue(event: MeseexEvent) -> None:
        events.put(event)

    unsubscribe = job.subscribe(enqueue, replay=True)
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
            _publish_runtime_event(event, tool_name, job)
            if event.kind is EventKind.SUCCEEDED:
                if tool_name == "run_agent":
                    return agent_turn_from_job(job)
                return serialize_job(job, event.result)
            if event.kind is EventKind.FAILED:
                raise event.error or RuntimeError("Job failed")
            if event.kind is EventKind.CANCELLED:
                return serialize_job(job)
    finally:
        unsubscribe()


def consume_or_serialize(method: Callable, result: Any) -> Any:
    if method in RUN_METHODS:
        return consume_job_sync(result, method.__name__)
    return serialize_value(result)


def bind_method(method: Callable, session: Optional[Callable] = None):
    """Bind an unbound client method to the active session and expose it without ``self``."""

    def invoke_sync(**arguments):
        from socaity import client

        with _session_scope(session):
            result = getattr(client, method.__name__)(**arguments)
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
