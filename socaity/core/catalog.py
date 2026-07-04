"""Public catalog functions of the socaity SDK.

Thin layer over the backend catalog API: list, get, search, connect.
List results are lazy (relations hydrate on first access), detail fetches
are complete. ``connect`` resolves any identifier through the backend and
returns a ready fastsdk client without installing a stub.
"""
from typing import Dict, List, Optional, Union

import fastsdk
from socaity_schemas.platform import AIModel, AIService, ServiceCategory

from socaity.core.lazy import LazyAIService, wrap_services
from socaity.core.socaity_backend_client import SocaityBackendClient

_client: Optional[SocaityBackendClient] = None


def _backend() -> SocaityBackendClient:
    global _client
    if _client is None:
        _client = SocaityBackendClient()
    return _client


def list_services(
    category: Optional[str] = None,
    limit: int = 100,
    offset: int = 0,
) -> List[LazyAIService]:
    """List public services (slim; relations load lazily on attribute access)."""
    return wrap_services(_backend().list_services(category=category, limit=limit, offset=offset), _backend())


def get_service(id_or_name: str) -> Optional[AIService]:
    """Fetch one service with deployments, endpoints and models embedded."""
    return _backend().get_service(id_or_name)


def list_models(
    family: Optional[str] = None,
    task: Optional[str] = None,
    limit: int = 100,
    offset: int = 0,
) -> List[AIModel]:
    """List AI models from the catalog."""
    return _backend().list_models(family=family, task=task, limit=limit, offset=offset)


def get_model(id_or_name: str) -> Optional[AIModel]:
    return _backend().get_model(id_or_name)


def list_categories() -> List[ServiceCategory]:
    return _backend().list_categories()


def search(query: str, collections: Optional[str] = None, limit: int = 20) -> List[Dict]:
    """Fuzzy search over services and models.

    Returns hits as dicts: {collection, id, score, document, highlights}.
    """
    return _backend().search(query, collections=collections, limit=limit)


def connect(source: Union[str, dict, AIService], api_key: Optional[str] = None, **kwargs) -> "fastsdk.FastClient":
    """Use a service without installing a stub.

    *source* can be anything fastsdk.connect accepts (URL, spec path/dict,
    AIService) or a socaity identifier (service name, UUID, 'user/service').
    Socaity identifiers resolve through the backend, so calls run over the
    inference gateway with your API key.
    """
    if isinstance(source, str) and not _looks_like_direct_source(source):
        item = _backend().install_service(source)
        service_data = (item or {}).get("service")
        if service_data:
            source = AIService(**service_data)
        # else: fall through, maybe fastsdk can resolve it (e.g. replicate ref)
    return fastsdk.connect(source, api_key=api_key, **kwargs)


def _looks_like_direct_source(source: str) -> bool:
    lowered = source.lower()
    return lowered.startswith(("http://", "https://", "replicate:")) or lowered.endswith(".json")
