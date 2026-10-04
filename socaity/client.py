"""Public SDK client: session-bound backend methods plus FastSDK job execution."""
from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import fastsdk
from fastsdk.fastClient import FastClient
from fastsdk.service_access import service_contract, set_reachability
from socaity_cli import SocaityBackendClient
from socaity_schemas.platform.catalog.service import Service
from socaity_schemas.platform.context import (
    SocaityContext,
    SocaityOptions,
)
from socaity_schemas.public.spec.address import SocaityServiceAddress

from socaity.core.gateway import gateway_client
from socaity.core.serialize import serialize_value


DEFAULT_APIPOD_GATE_URL = "https://api.socaity.ai"


def _gate_bind(service: Service, gate_url: str, details_id: Optional[str] = None) -> Service:
    """Point every binding at ``{gate}/services/v1/{slug_or_id}``.

    Marketplace ``sk_`` catalog reads redact origin addresses. The SDK always
    stamps the gate URL. Pinned ``details_id`` is first so FastSDK's primary
    binding is the one the caller asked for.
    """
    ident = service.slug or service.id
    if not ident:
        raise RuntimeError("Service has no slug or id.")
    address = SocaityServiceAddress(
        base_url=gate_url.rstrip("/"),
        path=f"/services/v1/{ident}",
        service_id=getattr(service, "id", None),
    )
    rows = list(service.details or [])
    if not rows:
        raise RuntimeError(f"Service '{ident}' has no details binding.")
    if details_id:
        pinned = [row for row in rows if row.id == details_id]
        if not pinned:
            raise RuntimeError(f"Service details '{details_id}' not found.")
        rows = pinned + [row for row in rows if row.id != details_id]
    updated = []
    for binding in rows:
        copy = binding.model_copy(deep=True)
        set_reachability(copy, provider="socaity", address=address)
        updated.append(copy)
    return service.model_copy(update={"details": updated})


def _target_candidates(target: str) -> list[tuple[str, Optional[str]]]:
    parts = [part for part in target.strip("/").split("/") if part]
    return [
        ("/".join(parts[:index]), ("/" + "/".join(parts[index:])) if index < len(parts) else None)
        for index in range(len(parts), 0, -1)
    ]


def _looks_like_direct_source(source: str) -> bool:
    lowered = source.lower()
    return lowered.startswith(("http://", "https://", "replicate:")) or lowered.endswith(".json")


def _resolve_endpoint(client: FastClient, endpoint: Optional[str]):
    """Pick the requested endpoint, or the service's first one when none was named."""
    endpoints = service_contract(client.service).endpoints
    if not endpoints:
        raise ValueError(f"Service '{client.service.slug or client.service.id}' exposes no endpoints.")
    if endpoint is None:
        return endpoints[0]

    wanted = endpoint if endpoint.startswith("/") else f"/{endpoint}"
    for candidate in endpoints:
        if candidate.path == wanted:
            return candidate
    known = ", ".join(candidate.path for candidate in endpoints)
    raise ValueError(f"Endpoint '{endpoint}' not found. This service exposes: {known}")


def _dump_model(raw: Any) -> Optional[dict]:
    """Dict or pydantic model to a JSON object. Empty stays empty."""
    if raw is None:
        return None
    if isinstance(raw, dict):
        return raw
    if hasattr(raw, "model_dump"):
        return raw.model_dump(mode="json", exclude_none=True)
    return None


def _inherit_context(explicit: Any, session: Any) -> Optional[SocaityContext]:
    """Explicit context wins per field. Thread falls back to the session conversation."""
    base = _dump_model(getattr(session, "socaity_context", None)) or {}
    over = _dump_model(explicit) or {}
    merged = {**base, **{key: value for key, value in over.items() if value is not None}}
    if not merged.get("thread_id"):
        conversation_id = getattr(session, "conversation_id", None)
        if conversation_id:
            merged["thread_id"] = conversation_id
    return SocaityContext.model_validate(merged) if merged else None


def job_flags(socaity_options: Any = None, socaity_context: Any = None) -> Dict[str, Any]:
    """Platform flags for a nested job. Explicit values win; the active session fills the rest."""
    from socaity.core.session import current_session
    session = current_session()
    flags: Dict[str, Any] = {}
    options = _dump_model(socaity_options if socaity_options is not None else getattr(session, "socaity_options", None))
    if options:
        flags["socaity_options"] = options
    context = _inherit_context(socaity_context, session)
    if context is not None:
        flags["socaity_context"] = context.model_dump(mode="json", exclude_none=True)
    return flags


class SocaityClient(SocaityBackendClient):
    """Session-scoped SDK client: CLI backend methods plus FastSDK job execution.

    Backend HTTP stays on the inherited mixins. ``connect``, ``run``,
    ``run_agent``, and ``run_workflow`` own payload construction; FastSDK owns
    submission, polling, cancel, and results.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        backend_url: Optional[str] = None,
        gate_url: Optional[str] = None,
        materialize_media: bool = True,
    ):
        super().__init__(backend_url=backend_url, api_key=api_key)
        env_gate = (os.environ.get("APIPOD_GATE_URL") or "").strip()
        self.gate_url = (gate_url or env_gate or DEFAULT_APIPOD_GATE_URL).rstrip("/")
        self.materialize_media = materialize_media

    def connect(
        self,
        source: Union[str, dict, Service, Path],
        api_key: Optional[str] = None,
        details_id: Optional[str] = None,
        **kwargs,
    ) -> FastClient:
        """Resolve a platform service or spec source into a FastSDK client.

        Platform identifiers (id, slug, ``owner/service``, details id) resolve
        through catalog ``get_service``. The binding is pointed at this session's
        gate. URLs, spec files, and ``replicate:`` refs go to FastSDK.

        Args:
            source: Service id, slug, URL, spec, or ``Service``.
            api_key: Override the session credential for this client.
            details_id: Pin one ``ServiceDetails`` binding.

        Returns:
            A credential-bound ``FastClient``.
        """
        resolved_key = api_key if api_key is not None else self.api_key
        if isinstance(source, Service):
            service = source
        elif isinstance(source, str) and not _looks_like_direct_source(source):
            service = self.get_service(details_id or source)
            if service is None:
                raise RuntimeError(f"Platform could not resolve service '{details_id or source}'.")
        else:
            kwargs.setdefault("materialize_media", self.materialize_media)
            return FastClient(source, api_key=resolved_key, temporary=True, **kwargs)

        service = _gate_bind(service, self.gate_url, details_id)
        kwargs.setdefault("materialize_media", self.materialize_media)
        return FastClient(service, api_key=resolved_key, temporary=True, **kwargs)

    def run(
        self,
        target: str,
        params: Optional[dict] = None,
        details_id: Optional[str] = None,
        socaity_options: Optional[Union[SocaityOptions, dict]] = None,
        socaity_context: Optional[Union[SocaityContext, dict]] = None,
        **kwargs,
    ) -> fastsdk.APISeex:
        """Submit a catalog service job.

        Agents use ``run_agent``. Workflows use ``run_workflow``.

        Args:
            target: ``{slug_or_id}/{path}`` or a bare slug (first contract endpoint).
            params: Endpoint arguments. ``**kwargs`` merge on top.
            details_id: Pin one ``ServiceDetails`` binding.
            socaity_options: Platform retention and visibility.
            socaity_context: Workflow, node, thread, and run-once slot names.

        Returns:
            FastSDK job handle. Call ``get_result()`` or ``subscribe`` yourself.
        """
        head = target.strip("/").split("/")[0] if target else ""
        if head.startswith(("wf_", "wr_")):
            raise ValueError(f"'{target}' is a workflow. Use run_workflow.")

        service = None
        remainder = None
        for key, path in _target_candidates(target):
            service = self.get_service(key)
            if service is not None:
                remainder = path
                break
        if service is None:
            raise RuntimeError(f"Service '{target}' not found.")
        if service.kind == "agent":
            raise ValueError(f"'{service.slug or service.id}' is an agent. Use run_agent.")

        client = self.connect(service, details_id=details_id)
        endpoint = _resolve_endpoint(client, remainder)
        job_params = {**(params or {}), **kwargs}
        if details_id:
            job_params["details_id"] = details_id
        return client.submit_job(endpoint.path, **{**job_params, **job_flags(socaity_options, socaity_context)})

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
            agent: Agent service id, slug, or ``owner/service``.
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
        body.update(job_flags())

        if supersedes_job_id:
            prior = self.track_job(supersedes_job_id)
            prior.cancel(action="interrupt")
            try:
                prior.get_result()
            except Exception:
                if not prior.is_terminal:
                    raise

        path = f"/v1/agents/{agent}/chat"
        client = gateway_client(self.gate_url, self.api_key, path, self.materialize_media)
        return client.submit_job(path, **{key: value for key, value in body.items() if value is not None})

    def run_workflow(
        self,
        workflow: str,
        inputs: Optional[dict] = None,
        revision_id: Optional[str] = None,
        version: Optional[int] = None,
        workflow_run_id: Optional[str] = None,
        stream: bool = False,
        entry_nodes: Optional[list] = None,
        scope_nodes: Optional[list] = None,
        seed_outputs: Optional[dict] = None,
    ) -> fastsdk.APISeex:
        """Submit a workflow run to ``POST /v1/workflows/{id}/run``.

        Args:
            workflow: Workflow id (``wf_...``), slug, or a run id (``wr_...``).
            inputs: Root node parameters. A flat dict applies to every entry node;
                nest a dict under a node id to target that node alone.
            revision_id: Revision to run (``rv_...``). Defaults to the latest valid.
            version: Valid version number as an alternative to ``revision_id``.
            workflow_run_id: Earlier run id (``wr_...``) to continue or resume.
            stream: Stream run events over the job SSE channel.
            entry_nodes: Enter the graph at these node ids instead of the roots (partial run).
            scope_nodes: Limit the walk to these node ids; one id is a single-step run.
            seed_outputs: Outputs keyed by node id for upstream nodes that do not run.

        Returns:
            FastSDK job handle for the gateway factory job.
        """
        workflow_id = workflow
        if workflow.startswith("wr_"):
            workflow_run_id = workflow_run_id or workflow
            run = self.get_workflow_run(workflow)
            if run is not None and getattr(run, "workflow_id", None):
                workflow_id = run.workflow_id
        path = f"/v1/workflows/{workflow_id}/run"
        client = gateway_client(self.gate_url, self.api_key, path, self.materialize_media)
        body = {
            "inputs": inputs or {},
            "revision_id": revision_id,
            "version": version,
            "workflow_run_id": workflow_run_id,
            "stream": stream,
            "entry_nodes": entry_nodes,
            "scope_nodes": scope_nodes,
            "seed_outputs": seed_outputs,
            **job_flags(),
        }
        return client.submit_job(path, **{key: value for key, value in body.items() if value is not None})

    def estimate_price(
        self,
        service: str,
        endpoint: Optional[str] = None,
        params: Optional[dict] = None,
    ) -> dict:
        """Estimate price and runtime of a job before running it.

        Args:
            service: Service id, slug, or ``owner/service``.
            endpoint: Endpoint path. Defaults to the service's first endpoint.
            params: The arguments you intend to pass to ``run``.

        Returns:
            Estimated cost, currency, and runtime for the endpoint.
        """
        client = self.connect(service)
        target = _resolve_endpoint(client, endpoint)
        estimate = client.estimate(target.path, **(params or {}))
        if estimate is None:
            raise ValueError(f"No estimate available for {service}{target.path}.")
        return estimate.model_dump(mode="json")

    def track_job(self, job_id: str) -> fastsdk.APISeex:
        """Re-attach to a running gateway job by id."""
        client = gateway_client(
            self.gate_url, self.api_key, f"/status/{job_id}", self.materialize_media
        )
        return client.track_job(job_id)

    def cancel_job(self, job_id: str, action: str = "cancel") -> dict:
        """Cancel or interrupt a running gateway job.

        Args:
            job_id: Platform job id from ``run``, ``run_agent``, or ``run_workflow``.
            action: ``cancel`` (default, user stop) or ``interrupt`` (HIT: resumable).

        Returns:
            The provider cancel summary.
        """
        job = self.track_job(job_id)
        return serialize_value(job.cancel(action=action))
