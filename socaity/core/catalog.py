"""Public catalog functions of the socaity SDK.

Thin layer over the backend catalog API: list, get, search, connect.
List results are lazy (relations hydrate on first access). ``connect`` resolves
any identifier through the backend and returns a ready fastsdk client.
"""
from typing import List, Optional, Union

import fastsdk
from socaity_schemas.platform import AIModel, AIService, Job, ServiceCategory
from socaity_cli import SocaityBackendClient

from socaity.core.lazy import LazyAIService, wrap_services
from socaity.core.session import current_session


def _backend() -> SocaityBackendClient:
    """Backend client of the active session (see ``socaity.core.session``)."""
    return current_session().backend


def list_services(
    category: Optional[str] = None,
    limit: int = 100,
    offset: int = 0,
    q: Optional[str] = None,
    filters: Optional[List[str]] = None,
    expand: Optional[List[str]] = None,
    fields: Optional[List[str]] = None,
    sort: Optional[str] = None,
    mine: bool = False,
) -> List[LazyAIService]:
    """List public services (slim by default; relations load lazily on attribute access)."""
    if q or filters or expand or fields or sort or mine:
        service_filters = list(filters or [])
        if category:
            service_filters.append(f"categories:contains:{category}")
        services = _backend().query_services(
            q=q,
            filters=service_filters or None,
            expand=expand,
            fields=fields,
            sort=sort,
            limit=limit,
            offset=offset,
            mine=mine,
        )
    else:
        services = _backend().list_services(category=category, limit=limit, offset=offset)
    return wrap_services(services, _backend())


def get_service(
    id_or_name: str,
    expand: Optional[List[str]] = None,
    fields: Optional[List[str]] = None,
    filters: Optional[List[str]] = None,
) -> Optional[AIService]:
    """Fetch one service; default expand embeds deployments, endpoints and models."""
    return _backend().get_service(id_or_name, expand=expand, fields=fields, filters=filters)


def list_models(
    family: Optional[str] = None,
    task: Optional[str] = None,
    limit: int = 100,
    offset: int = 0,
    q: Optional[str] = None,
    filters: Optional[List[str]] = None,
    expand: Optional[List[str]] = None,
    fields: Optional[List[str]] = None,
    sort: Optional[str] = None,
) -> List[AIModel]:
    """List AI models from the catalog."""
    if q or filters or expand or fields or sort:
        return _backend().query_models(
            q=q,
            filters=filters,
            expand=expand,
            fields=fields,
            sort=sort,
            limit=limit,
            offset=offset,
        )
    return _backend().list_models(family=family, task=task, limit=limit, offset=offset)


def get_model(id_or_name: str, expand: Optional[List[str]] = None) -> Optional[AIModel]:
    return _backend().get_model(id_or_name, expand=expand)


def list_categories() -> List[ServiceCategory]:
    return _backend().list_categories()


def list_pricing_rules(active_only: bool = True) -> list:
    """Active hosting pricing rules from the catalog."""
    return _backend().list_pricing_rules(active_only=active_only)


def search(
    query: str,
    collection: str = "services",
    filters: Optional[List[str]] = None,
    limit: int = 20,
    visibility: str = "user_visible",
) -> List[Union[AIService, AIModel, Job]]:
    """Fuzzy search over services, models, or jobs (backend ``q`` param)."""
    return _backend().search(
        query, collection=collection, filters=filters, limit=limit, visibility=visibility,
    )


def connect(source: Union[str, dict, AIService], api_key: Optional[str] = None, **kwargs) -> "fastsdk.FastClient":
    """Use a service without installing a stub.

    Platform services resolve through the backend and inherit the session credential,
    so a multi-tenant host never falls back to a process-wide environment key. Direct
    sources (URLs, Replicate refs, spec files) keep fastsdk's own key resolution.
    """
    session = current_session()
    is_platform_service = isinstance(source, str) and not _looks_like_direct_source(source)

    if is_platform_service:
        item = session.backend.install_service(source)
        service_data = (item or {}).get("service")
        if service_data:
            source = AIService(**service_data)
        api_key = api_key or session.api_key

    kwargs.setdefault("materialize_media", session.materialize_media)
    return fastsdk.connect(source, api_key=api_key, **kwargs)


def _looks_like_direct_source(source: str) -> bool:
    lowered = source.lower()
    return lowered.startswith(("http://", "https://", "replicate:")) or lowered.endswith(".json")
