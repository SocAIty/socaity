"""FastMCP server exposing Socaity catalog, jobs, chats, projects, and run_service."""
from __future__ import annotations

import os
from typing import Any, Dict, List, Optional

# Keep job file URLs as refs; agents download via get_files.
os.environ.setdefault("FASTSDK_MATERIALIZE_MEDIA", "0")

from socaity.core import catalog as catalog_api
from socaity.core import jobs as jobs_api
from socaity.core import projects as projects_api
from socaity.integrations.mcp import auth as mcp_auth
from socaity.integrations.mcp.call import run_call
from socaity.integrations.mcp.files import get_files as fetch_files
from socaity.integrations.mcp.playbook import AGENT_PLAYBOOK
from socaity.integrations.mcp.rate_limit import limiter
from socaity.integrations.mcp.serialize import to_jsonable
from socaity_cli import SocaityBackendClient

try:
    from fastmcp import FastMCP
except ImportError as exc:  # pragma: no cover
    raise ImportError(
        "fastmcp is required for the Socaity MCP server. Install with: pip install 'socaity[mcp]'"
    ) from exc


def create_mcp(name: str = "socaity") -> FastMCP:
    mcp = FastMCP(
        name,
        instructions=AGENT_PLAYBOOK,
    )

    def _gated() -> None:
        limiter.check()

    @mcp.tool
    def login(no_browser: bool = False, timeout: int = 300) -> Dict[str, Any]:
        """Open the Socaity browser login flow and store a temporary API key (tk_).

        Same mechanism as `socaity login`. Prefer SOCAITY_API_KEY in CI.
        """
        _gated()
        return mcp_auth.login(no_browser=no_browser, timeout=timeout)

    @mcp.tool
    def whoami() -> Dict[str, Any]:
        """Return the authenticated user id, email, and backend URL."""
        _gated()
        mcp_auth.ensure_api_key()
        return mcp_auth.whoami()

    @mcp.tool
    def search_services(
        q: str,
        limit: int = 10,
        filters: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        """Fuzzy-search AI services. Use short keywords (sdxl, flux, tts, qwen), not long intents.

        Rank by relevance then prefer higher n_usages / official. Example filters:
        categories:contains:image , is_official:eq:true
        """
        _gated()
        mcp_auth.ensure_api_key()
        rows = catalog_api.list_services(q=q, filters=filters, limit=limit)
        return [to_jsonable(getattr(r, "raw", None) or r) for r in rows]

    @mcp.tool
    def list_services(
        category: Optional[str] = None,
        limit: int = 20,
        offset: int = 0,
    ) -> List[Dict[str, Any]]:
        """List catalog services (optional category slug)."""
        _gated()
        mcp_auth.ensure_api_key()
        rows = catalog_api.list_services(category=category, limit=limit, offset=offset)
        return [to_jsonable(getattr(r, "raw", None) or r) for r in rows]

    @mcp.tool
    def get_service(id_or_name: str) -> Dict[str, Any]:
        """Fetch one service with endpoints, deployments, and models. Required before run_service."""
        _gated()
        mcp_auth.ensure_api_key()
        svc = catalog_api.get_service(id_or_name, expand=["endpoints", "deployments", "models"])
        if svc is None:
            raise ValueError(f"Service not found: {id_or_name}")
        return to_jsonable(svc)

    @mcp.tool
    def search_models(
        q: str,
        limit: int = 10,
        filters: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        """Fuzzy-search AI models. Then find services that implement the model via get_model expand."""
        _gated()
        mcp_auth.ensure_api_key()
        rows = catalog_api.list_models(q=q, filters=filters, limit=limit)
        return [to_jsonable(r) for r in rows]

    @mcp.tool
    def get_model(id_or_name: str) -> Dict[str, Any]:
        """Fetch one model; expand services that implement it when available."""
        _gated()
        mcp_auth.ensure_api_key()
        model = catalog_api.get_model(id_or_name, expand=["services"])
        if model is None:
            raise ValueError(f"Model not found: {id_or_name}")
        return to_jsonable(model)

    @mcp.tool
    def list_jobs(
        q: Optional[str] = None,
        limit: int = 20,
        offset: int = 0,
    ) -> List[Dict[str, Any]]:
        """List or fuzzy-search the caller's jobs."""
        _gated()
        mcp_auth.ensure_api_key()
        rows = jobs_api.list_jobs(q=q, limit=limit, offset=offset)
        return [to_jsonable(r) for r in rows]

    @mcp.tool
    def get_job(job_id: str) -> Dict[str, Any]:
        """Get one job with data + files expands (file URLs, not bytes)."""
        _gated()
        mcp_auth.ensure_api_key()
        job = jobs_api.get_job(job_id, expand=["data", "files", "billing"])
        if job is None:
            raise ValueError(f"Job not found: {job_id}")
        return to_jsonable(job)

    @mcp.tool
    def list_projects(limit: int = 20, offset: int = 0) -> List[Dict[str, Any]]:
        """List projects visible to the caller."""
        _gated()
        mcp_auth.ensure_api_key()
        rows = projects_api.list_projects(limit=limit, offset=offset)
        return [to_jsonable(r) for r in rows]

    @mcp.tool
    def get_project(project_id: str) -> Dict[str, Any]:
        """Fetch one project by id."""
        _gated()
        mcp_auth.ensure_api_key()
        project = projects_api.get_project(project_id)
        if project is None:
            raise ValueError(f"Project not found: {project_id}")
        return to_jsonable(project)

    @mcp.tool
    def list_chats(
        q: Optional[str] = None,
        limit: int = 20,
        offset: int = 0,
    ) -> List[Dict[str, Any]]:
        """List or Typesense-search conversations for the authenticated user."""
        _gated()
        mcp_auth.ensure_api_key()
        client = SocaityBackendClient()
        payload = client._get("v1/conversations", params={
            "q": q,
            "limit": limit,
            "offset": offset,
        })
        return to_jsonable(_unwrap_list(payload))

    @mcp.tool
    def get_chat(conversation_id: str, expand_items: bool = True) -> Dict[str, Any]:
        """Get one conversation; optionally expand chat items."""
        _gated()
        mcp_auth.ensure_api_key()
        client = SocaityBackendClient()
        params: Dict[str, Any] = {}
        if expand_items:
            params["expand"] = ["items"]
        row = client._get(f"v1/conversations/{conversation_id}", params=params)
        if not row:
            raise ValueError(f"Conversation not found: {conversation_id}")
        return to_jsonable(row)

    @mcp.tool
    def run_service(
        call: str,
        args: Optional[Dict[str, Any]] = None,
        wait: bool = True,
        timeout_s: float = 600.0,
    ) -> Dict[str, Any]:
        """Execute any platform AI service endpoint.

        Call syntax: `service@/endpoint` where service is catalog name/id
        (may contain `/`) and endpoint is the OpenAPI path.

        Example: call="bytedance/sdxl-lightning-4step@/predict"
                 args={"prompt": "a cute robot dog"}

        Results include file URLs only. Use get_files to download.
        """
        _gated()
        return run_call(call, args=args, wait=wait, timeout_s=timeout_s)

    @mcp.tool
    def get_files(
        job_id: Optional[str] = None,
        url: Optional[str] = None,
        file_id: Optional[int] = None,
        save_path: Optional[str] = None,
    ) -> Dict[str, Any]:
        """List and/or download files from a job result URL.

        Prefer url from run_service/get_job. Set save_path to write bytes to disk.
        Example: get_files(url="https://...", save_path="./robot-dog.png")
        """
        _gated()
        return fetch_files(job_id=job_id, url=url, file_id=file_id, save_path=save_path)

    @mcp.resource("socaity://playbook")
    def playbook() -> str:
        """Full agent playbook for discovery, call syntax, and media workflows."""
        return AGENT_PLAYBOOK

    return mcp


def _unwrap_list(payload: Any) -> Any:
    if isinstance(payload, dict) and "entities" in payload:
        return payload.get("entities") or []
    if isinstance(payload, list):
        return payload
    return payload or []


mcp = create_mcp()
