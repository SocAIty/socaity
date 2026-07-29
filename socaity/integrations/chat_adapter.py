"""Framework-neutral chat access to one platform service.

``ChatServiceAdapter`` hides the platform protocol behind three calls:
``complete`` (blocking), ``stream_chunks`` / ``astream_chunks`` (typed
OpenAI-style chunk dicts). Framework adapters (LangChain, LlamaIndex, ...)
subclass or compose it and only translate between the framework's message
types and the OpenAI-compatible wire format of ``socaity_schemas``.

Every call runs as a platform job (APISeex). The adapter keeps the handles
of the jobs it submitted so frameworks can inspect progress, metrics and
platform job ids without touching fastSDK internals.
"""
from __future__ import annotations

from typing import Any, AsyncIterator, Dict, Iterator, List, Optional, Union

from fastsdk import APISeex, FastClient
from fastsdk.service_access import service_contract
from socaity_schemas.contract import Endpoint
from socaity_schemas.platform import AIService

from socaity.core.catalog import connect

CHAT_SCHEMA_NAME = "ChatCompletionRequest"


class ChatServiceAdapter:
    """One chat-capable platform service, spoken to in OpenAI wire shapes.

    Args:
        service: Service slug, id, URL, ``AIService`` or an existing
            ``FastClient`` (reused as-is).
        api_key: Socaity API key; falls back to the stored login.
        endpoint_path: Chat endpoint path override. Default: the endpoint
            implementing ``ChatCompletionRequest``, else ``/chat``.
    """

    def __init__(
        self,
        service: Union[str, dict, AIService, FastClient],
        api_key: Optional[str] = None,
        endpoint_path: Optional[str] = None,
    ):
        self.client = service if isinstance(service, FastClient) else connect(service, api_key=api_key)
        self.endpoint = self._resolve_chat_endpoint(endpoint_path)
        self.jobs: List[APISeex] = []

    @property
    def service(self) -> AIService:
        return self.client.service

    # ------------------------------------------------------------------
    # Endpoint resolution
    # ------------------------------------------------------------------

    def _resolve_chat_endpoint(self, endpoint_path: Optional[str]) -> Endpoint:
        contract = service_contract(self.service)
        if endpoint_path:
            for endpoint in contract.endpoints:
                if endpoint.path == endpoint_path:
                    return endpoint
            raise ValueError(f"Service {self.service.name} has no endpoint {endpoint_path!r}.")

        # Prefer the declared standard schema; VLM chat endpoints subclass the
        # schema (VLMChatRequest) and are found via the conventional /chat path.
        for endpoint in contract.endpoints:
            if endpoint.standard_schema == CHAT_SCHEMA_NAME:
                return endpoint
        for endpoint in contract.endpoints:
            if endpoint.path == "/chat":
                return endpoint
        raise ValueError(
            f"Service {self.service.name} exposes no chat endpoint "
            f"(no {CHAT_SCHEMA_NAME} schema and no /chat path)."
        )

    # ------------------------------------------------------------------
    # Calls
    # ------------------------------------------------------------------

    def submit(self, request: Dict[str, Any]) -> APISeex:
        """Submit one chat request as a platform job and record the handle."""
        job = self.client.submit_job(self.endpoint.path, **self._job_kwargs(request))
        self.jobs.append(job)
        return job

    def _job_kwargs(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Map the OpenAI request dict onto the endpoint's call signature.

        Platform contracts materialise schema endpoints as one required body
        parameter named ``request``. Local APIPod OpenAPI often flattens the
        ChatCompletionRequest fields instead. Match whichever shape the
        resolved endpoint declares.
        """
        params = list(self.endpoint.parameters or [])
        if len(params) == 1 and getattr(params[0], "name", None) == "request":
            return {"request": request}
        return dict(request)

    def complete(self, request: Dict[str, Any], timeout_s: Optional[float] = None) -> Dict[str, Any]:
        """Blocking chat completion; returns a ChatCompletionResponse-shaped dict."""
        job = self.submit({**request, "stream": False})
        return self._as_response_dict(job.get_result(timeout_s=timeout_s))

    def stream_chunks(self, request: Dict[str, Any]) -> Iterator[Dict[str, Any]]:
        """Stream ChatCompletionChunk-shaped dicts (sync)."""
        job = self.submit({**request, "stream": True})
        session = job.stream()
        try:
            for chunk in session.iter_chunks():
                yield self._as_chunk_dict(chunk)
        finally:
            session.close()

    async def astream_chunks(self, request: Dict[str, Any]) -> AsyncIterator[Dict[str, Any]]:
        """Stream ChatCompletionChunk-shaped dicts (async)."""
        job = self.submit({**request, "stream": True})
        session = job.stream()
        try:
            async for chunk in session.aiter_chunks():
                yield self._as_chunk_dict(chunk)
        finally:
            session.close()

    # ------------------------------------------------------------------
    # Job introspection
    # ------------------------------------------------------------------

    @staticmethod
    def job_status(job: APISeex) -> Dict[str, Any]:
        """Progress/status snapshot of one submitted job."""
        response = job.response
        progress = job.task_progress
        return {
            "job_id": getattr(response, "job_id", None) or getattr(response, "id", None),
            "status": getattr(response, "status", None),
            "is_terminal": job.is_terminal,
            "progress": getattr(progress, "percent", None),
            "error": getattr(response, "error", None),
        }

    def last_job(self) -> Optional[APISeex]:
        return self.jobs[-1] if self.jobs else None

    # ------------------------------------------------------------------
    # Result normalization
    # ------------------------------------------------------------------

    @staticmethod
    def _as_response_dict(result: Any) -> Dict[str, Any]:
        """Normalize a job result into a ChatCompletionResponse-shaped dict."""
        if isinstance(result, dict) and "choices" in result:
            return result
        if hasattr(result, "model_dump"):
            dumped = result.model_dump()
            if isinstance(dumped, dict) and "choices" in dumped:
                return dumped
        if isinstance(result, str):
            return {"choices": [{"index": 0, "message": {"role": "assistant", "content": result}, "finish_reason": "stop"}]}
        raise ValueError(f"Unexpected chat result shape: {type(result).__name__}")

    @staticmethod
    def _as_chunk_dict(chunk: Any) -> Dict[str, Any]:
        """Normalize one SSE item into a ChatCompletionChunk-shaped dict."""
        if isinstance(chunk, dict):
            return chunk
        # Tolerate plain-text SSE data lines from non-standard services.
        return {"choices": [{"index": 0, "delta": {"content": str(chunk)}, "finish_reason": None}]}
