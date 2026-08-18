"""Agent tool registry: name -> callable, wired from socaity.core + compact views.

No per-SDK-tool wrapper modules. Implementations live here only where the agent
needs a different JSON shape or parameter names than the public SDK helpers.
Execution tools stay in ``run.py``.
"""

from __future__ import annotations

from typing import Callable, List, Optional

from fastsdk.service_access import service_contract

from socaity.core import catalog, files, jobs
from socaity.tools.run import estimate_price, run_service
from socaity.tools.serialize import job_summary, page, service_detail, service_summary

ENDPOINT_EXPAND = ["deployments.contract", "endpoints", "models"]
JOB_EXPAND = ["files", "billing", "data"]


def _tool(name: str, doc: str, fn: Callable) -> Callable:
    fn.__name__ = name
    fn.__doc__ = doc
    return fn


def _search_services(
    query: Optional[str] = None,
    category: Optional[str] = None,
    filters: Optional[List[str]] = None,
    expand: Optional[List[str]] = None,
    fields: Optional[List[str]] = None,
    sort: Optional[str] = None,
    limit: int = 20,
    offset: int = 0,
    mine: bool = False,
) -> dict:
    rows = catalog.list_services(
        q=query,
        category=category,
        filters=filters,
        expand=expand,
        fields=fields,
        sort=sort,
        limit=limit,
        offset=offset,
        mine=mine,
    )
    return page([service_summary(row) for row in rows], limit, offset)


def _get_service(
    identifier: str,
    expand: Optional[List[str]] = None,
    fields: Optional[List[str]] = None,
    filters: Optional[List[str]] = None,
) -> dict:
    service = catalog.get_service(
        identifier,
        expand=expand if expand is not None else ENDPOINT_EXPAND,
        fields=fields,
        filters=filters,
    )
    if service is None:
        return {"found": False, "identifier": identifier}
    try:
        endpoints = service_contract(getattr(service, "raw", service)).endpoints
    except ValueError:
        endpoints = []
    return {"found": True, **service_detail(service, endpoints)}


def _get_job(job_id: str) -> dict:
    job = jobs.get_job(job_id, expand=JOB_EXPAND)
    if job is None:
        return {"found": False, "job_id": job_id}
    return {"found": True, **job_summary(job)}


def _list_files(
    purpose: Optional[List[str]] = None,
    include_expired: bool = False,
    limit: int = 20,
    offset: int = 0,
) -> dict:
    rows = files.list_files(
        purpose=purpose or ["USER_UPLOAD", "JOB_RESULT"],
        include_expired=include_expired,
        limit=limit,
        offset=offset,
    )
    return page(rows, limit, offset)


_SEARCH_DOC = """Find AI services in the socaity catalog. Start here for any generation task.

Search by capability: "text to image", "voice cloning", "upscale".
Results are slim. Call ``get_service`` with the hit ``id`` for the call signature.

Args:
    query: Free-text search. Omit to browse.
    category: Category id. The catalog filters on ids, not display names.
    filters: ``field:operator:value`` strings.
    expand: Relations to embed (``deployments``, ``models``, ``pricing``).
    fields: Sparse fieldset, e.g. ``["id", "name"]``.
    sort: ``field:asc`` or ``field:desc``.
    limit: Results per page, 1 to 100.
    offset: Results to skip. Use ``next_offset`` from the previous page.
    mine: Only services created by the caller.

Returns:
    A page of service summaries.
"""

_GET_SERVICE_DOC = """Fetch one catalog service by id, name, or "owner/service".

Default expand embeds deployments, endpoints and models so you can call
``run_service``. Endpoint ``parameters`` are the keys ``params`` accepts.

Args:
    identifier: Service id or name from search_services.
    expand: Override the default expand list.
    fields: Sparse fieldset.
    filters: Post-fetch filters.

Returns:
    Service metadata and endpoints, or ``found: false``.
"""

_GET_JOB_DOC = """Read one job: its status, result files, runtime and cost.

Poll this after run_service returned status "running", or to retrieve the output
of a job you started earlier.

Args:
    job_id: Platform job id, as returned by run_service or list_jobs.

Returns:
    Job details including ``files`` with result URLs.
"""

_LIST_FILES_DOC = """List the caller's stored files with download URLs.

Args:
    purpose: Filter, e.g. ``["USER_UPLOAD", "JOB_RESULT"]``. Default: both.
    include_expired: Include files past expires_at.
    limit: Page size, 1 to 100.
    offset: Skip this many. Use ``next_offset`` from the previous page.

Returns:
    A page of file records. ``url`` on each record is downloadable.
"""

REGISTRY: dict[str, Callable] = {
    "search_services": _tool("search_services", _SEARCH_DOC, _search_services),
    "get_service": _tool("get_service", _GET_SERVICE_DOC, _get_service),
    "run_service": run_service,
    "estimate_price": estimate_price,
    "get_job": _tool("get_job", _GET_JOB_DOC, _get_job),
    "list_files": _tool("list_files", _LIST_FILES_DOC, _list_files),
}

TOOLS: tuple[Callable, ...] = tuple(REGISTRY.values())

search_services = REGISTRY["search_services"]
get_service = REGISTRY["get_service"]
get_job = REGISTRY["get_job"]
list_files = REGISTRY["list_files"]
