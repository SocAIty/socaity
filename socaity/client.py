"""Public SDK client: session-bound backend methods plus FastSDK job execution."""
from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import fastsdk
from fastsdk.fastClient import FastClient
from fastsdk.service_access import service_contract
from socaity_cli import SocaityBackendClient
from socaity_schemas.platform import AIService

from socaity.core.serialize import serialize_value

DEFAULT_APIPOD_GATE_URL = "https://api.socaity.ai"


def _looks_like_direct_source(source: str) -> bool:
    lowered = source.lower()
    return lowered.startswith(("http://", "https://", "replicate:")) or lowered.endswith(".json")


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
    """Merge caller params with job flags the endpoint actually accepts."""
    call = dict(params or {})
    accepted = {parameter.name for parameter in endpoint.parameters}
    call.update({name: value for name, value in flags.items() if name in accepted})
    return call


class SocaityClient(SocaityBackendClient):
    """Session-scoped SDK client: CLI backend methods plus FastSDK job execution.

    Backend HTTP stays on the inherited mixins. ``connect`` and ``run_*`` own
    payload construction; FastSDK owns submission, polling, cancel, and results.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        backend_url: Optional[str] = None,
        gate_url: Optional[str] = None,
        materialize_media: bool = True,
    ):
        super().__init__(backend_url=backend_url, api_key=api_key)
        self.gate_url = (gate_url or os.environ.get("APIPOD_GATE_URL") or DEFAULT_APIPOD_GATE_URL).rstrip("/")
        self.materialize_media = materialize_media

    def connect(self, source: Union[str, dict, AIService, Path], api_key: Optional[str] = None, **kwargs) -> FastClient:
        """Resolve a platform service or spec source into a FastSDK client.

        Platform identifiers (id, slug, ``owner/service``) resolve through
        ``install_service``. URLs, spec files, and ``replicate:`` refs go to FastSDK.

        Args:
            source: Service id, name, URL, spec, or ``AIService``.
            api_key: Override the session credential for this client.

        Returns:
            A credential-bound ``FastClient``.
        """
        resolved_key = api_key if api_key is not None else self.api_key
        is_platform = isinstance(source, str) and not _looks_like_direct_source(source)
        if is_platform:
            item = self.install_service(source)
            service_data = (item or {}).get("service")
            if not service_data:
                raise RuntimeError(f"Platform could not resolve service '{source}'.")
            source = AIService(**service_data)
        kwargs.setdefault("materialize_media", self.materialize_media)
        return FastClient(source, api_key=resolved_key, temporary=False, **kwargs)

    def run_service(
        self,
        service: str,
        endpoint: Optional[str] = None,
        params: Optional[dict] = None,
        is_public: bool = False,
        expires_at: Optional[str] = None,
    ) -> fastsdk.APISeex:
        """Submit a catalog service job. Returns an ``APISeex`` handle immediately.

        Call ``get_service`` (expand ``deployments.contract``) when you do not know
        the parameter names. ``params`` keys must match that endpoint exactly.

        Args:
            service: Service id, name, ``owner/service``, or model slug.
            endpoint: Endpoint path such as ``/predictions``. Defaults to the first.
            params: Endpoint arguments, e.g. ``{"prompt": "a cute robot dog"}``.
            is_public: Publish the job in the socaity feed. Default private.
            expires_at: Optional ISO timestamp for produced files.

        Returns:
            FastSDK job handle. Call ``get_result()`` or ``subscribe`` yourself.
            LLM tool conversion waits for the terminal event and serializes it.
        """
        client = self.connect(service)
        target = _resolve_endpoint(client, endpoint)
        return client.submit_job(
            target.path,
            **_call_params(target, params, {"is_public": is_public, "expires_at": expires_at}),
        )

    def estimate_price(
        self,
        service: str,
        endpoint: Optional[str] = None,
        params: Optional[dict] = None,
    ) -> dict:
        """Estimate price and runtime of a job before running it.

        Args:
            service: Service id, name, or ``owner/service``.
            endpoint: Endpoint path. Defaults to the service's first endpoint.
            params: The arguments you intend to pass to ``run_service``.

        Returns:
            Estimated cost, currency, and runtime for the endpoint.
        """
        client = self.connect(service)
        target = _resolve_endpoint(client, endpoint)
        estimate = client.estimate(target.path, **(params or {}))
        if estimate is None:
            raise ValueError(f"No estimate available for {service}{target.path}.")
        return estimate.model_dump(mode="json")

    def run_agent(
        self,
        agent: str,
        message: Optional[str] = None,
        messages: Optional[List[dict]] = None,
        thread_id: Optional[str] = None,
        mode: Optional[str] = None,
        model: Optional[str] = None,
        decisions: Optional[List[dict]] = None,
        continue_turn: bool = False,
        supersedes_job_id: Optional[str] = None,
        parent_item_id: Optional[str] = None,
        workflow: Optional[dict] = None,
    ) -> fastsdk.APISeex:
        """Submit one agent turn to ``POST /v1/agents/{id}/chat``.

        Args:
            agent: Agent service id, name, or ``owner/service``.
            message: Convenience single user message; appended to ``messages``.
            messages: Full ChatCompletion message list for the turn.
            thread_id: Conversation thread; reuse it to continue or resume.
            mode: Agent mode (SPAINE: chat | plan | agent | repair).
            model: Model override passed through to the agent.
            decisions: HIT decisions answering a previous ``pending_actions`` batch.
            continue_turn: After a cancel, invoke from the last checkpoint.
            supersedes_job_id: Live agent job this turn replaces (interrupted first).
            parent_item_id: Edit-and-fork parent of the new user message.
            workflow: Workflow document draft to seed the agent with.

        Returns:
            FastSDK job handle for the gateway factory job.
        """
        turn_messages = list(messages or [])
        if message:
            turn_messages.append({"role": "user", "content": message})
        if continue_turn:
            if not thread_id:
                raise ValueError("continue_turn requires the thread_id of the cancelled turn.")
            if turn_messages or decisions:
                raise ValueError("continue_turn takes no messages and no decisions.")
            if supersedes_job_id:
                raise ValueError("continue_turn cannot supersede a live job; omit supersedes_job_id.")
        elif not turn_messages and not decisions:
            raise ValueError("run_agent needs a message, messages, or decisions to resume with.")

        agent_config = {key: value for key, value in (("mode", mode), ("model", model)) if value}
        body: Dict[str, Any] = {"messages": turn_messages, "stream": False}
        if agent_config:
            body["agent"] = agent_config
        if continue_turn:
            body["continue"] = True
        if parent_item_id is not None:
            body["parent_item_id"] = parent_item_id
        for key, value in (("thread_id", thread_id), ("decisions", decisions), ("workflow", workflow)):
            if value:
                body[key] = value

        if supersedes_job_id:
            prior = self.track_job(supersedes_job_id)
            prior.cancel(action="interrupt")
            try:
                prior.get_result()
            except Exception:
                if not prior.is_terminal:
                    raise

        return fastsdk.submit_factory(
            f"/v1/agents/{agent}/chat",
            {key: value for key, value in body.items() if value is not None},
            address=self.gate_url,
            api_key=self.api_key,
            materialize_media=self.materialize_media,
        )

    def run_workflow(
        self,
        workflow: str,
        inputs: Optional[dict] = None,
        revision_id: Optional[str] = None,
        version: Optional[int] = None,
        workflow_run_id: Optional[str] = None,
        stream: bool = False,
    ) -> fastsdk.APISeex:
        """Submit a workflow run to ``POST /v1/workflows/{id}/run``.

        Args:
            workflow: Workflow id (``wf_...``) or slug.
            inputs: Workflow input values. Keys must match the document's inputs.
            revision_id: Revision to run (``rv_...``). Defaults to the latest valid.
            version: Valid version number as an alternative to ``revision_id``.
            workflow_run_id: Earlier run id (``wr_...``) to continue or resume.
            stream: Stream run events over the job SSE channel.

        Returns:
            FastSDK job handle for the gateway factory job.
        """
        return fastsdk.submit_factory(
            f"/v1/workflows/{workflow}/run",
            {
                "inputs": inputs or {},
                "revision_id": revision_id,
                "version": version,
                "workflow_run_id": workflow_run_id,
                "stream": stream,
            },
            address=self.gate_url,
            api_key=self.api_key,
            materialize_media=self.materialize_media,
        )

    def track_job(self, job_id: str) -> fastsdk.APISeex:
        """Re-attach to a running gateway job by id."""
        return fastsdk.track_job(
            job_id,
            address=self.gate_url,
            api_key=self.api_key,
            materialize_media=self.materialize_media,
        )

    def cancel_job(self, job_id: str, action: str = "cancel") -> dict:
        """Cancel or interrupt a running gateway job.

        Args:
            job_id: Platform job id from ``run_service``, ``run_agent``, or ``run_workflow``.
            action: ``cancel`` (default, user stop) or ``interrupt`` (HIT: resumable).

        Returns:
            The provider cancel summary.
        """
        job = self.track_job(job_id)
        return serialize_value(job.cancel(action=action))
