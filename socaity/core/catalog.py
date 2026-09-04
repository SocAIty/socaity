"""Public catalog functions of the socaity SDK.

Thin layer over the backend catalog API: query, get, connect.
Query results are lazy (relations hydrate on first access). ``connect`` resolves
any identifier through the backend and returns a ready fastsdk client.
"""
from typing import List, Optional, Union

import fastsdk
from fastsdk.fastClient import FastClient
from socaity_schemas.platform import AIModel, AIService, ServiceCategory
from socaity_cli import SocaityBackendClient

from socaity.core.lazy import LazyAIService, wrap_services
from socaity.core.session import current_session


def _backend() -> SocaityBackendClient:
    """Backend client of the active session (see ``socaity.core.session``)."""
    return current_session().backend


def query_services(
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
    """Query public services (slim by default; relations load lazily on attribute access)."""
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
    return wrap_services(services, _backend())


def get_service(
    id_or_name: str,
    expand: Optional[List[str]] = None,
    fields: Optional[List[str]] = None,
    filters: Optional[List[str]] = None,
) -> Optional[AIService]:
    """Fetch one service; default expand embeds deployments, endpoints and models."""
    return _backend().get_service(id_or_name, expand=expand, fields=fields, filters=filters)


def query_models(
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
    """Query AI models from the catalog."""
    return _backend().query_models(
        q=q,
        family=family,
        task=task,
        filters=filters,
        expand=expand,
        fields=fields,
        sort=sort,
        limit=limit,
        offset=offset,
    )


def get_model(id_or_name: str, expand: Optional[List[str]] = None) -> Optional[AIModel]:
    return _backend().get_model(id_or_name, expand=expand)


def query_categories() -> List[ServiceCategory]:
    return _backend().query_categories()


def list_pricing_rules(active_only: bool = True) -> list:
    """Active hosting pricing rules from the catalog."""
    return _backend().list_pricing_rules(active_only=active_only)


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
        if not service_data:
            raise RuntimeError(f"Platform could not resolve service '{source}'.")
        source = AIService(**service_data)
        api_key = api_key or session.api_key

    kwargs.setdefault("materialize_media", session.materialize_media)
    # install_service already points the deployment at the gateway
    # (`/services/v1/{deployment.id}`). Keep the client in the registry:
    # fastsdk.connect() is temporary and used to persist-delete the cache row.
    return FastClient(source, api_key=api_key, temporary=False, **kwargs)


def _looks_like_direct_source(source: str) -> bool:
    lowered = source.lower()
    return lowered.startswith(("http://", "https://", "replicate:")) or lowered.endswith(".json")
