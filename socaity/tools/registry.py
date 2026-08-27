"""Agent tool registry: CLI client methods bound to the active session."""

from __future__ import annotations

import inspect
from typing import Any, Callable, Type

from socaity.core.session import current_session
from socaity_cli.clients.catalog import CatalogClient
from socaity_cli.clients.files import FilesClient
from socaity_cli.clients.jobs import JobsClient
from socaity.tools.json import dump_entity
from socaity.tools.run import estimate_price, run_service

SERVICE_DETAIL_EXPAND = CatalogClient.SERVICE_DETAIL_EXPAND
JOB_DETAIL_EXPAND = JobsClient.JOB_DETAIL_EXPAND


def _tool(name: str, mixin: Type, method_name: str | None = None) -> Callable:
    """Expose one ``SocaityBackendClient`` mixin method as an agent tool.

    Docstring and signature come from the CLI mixin (ground truth). Returns are
    JSON-serializable; ``None`` means not found / no row (see each tool doc).
    """
    method_name = method_name or name
    source = getattr(mixin, method_name)

    def wrapper(*args, **kwargs):
        result = getattr(current_session().backend, method_name)(*args, **kwargs)
        dumped = dump_entity(result)
        if name == "search_services" and isinstance(dumped, list):
            dumped = [_slim_service(item) for item in dumped]
        return dumped

    wrapper.__name__ = name
    wrapper.__doc__ = inspect.getdoc(source)
    try:
        signature = inspect.signature(source)
        params = [param for param in signature.parameters.values() if param.name != "self"]
        wrapper.__signature__ = signature.replace(parameters=params)
    except (TypeError, ValueError):
        pass
    if hasattr(source, "__annotations__"):
        wrapper.__annotations__ = {
            key: value for key, value in source.__annotations__.items() if key != "self"
        }
    return wrapper


REGISTRY: dict[str, Callable] = {
    "search_services": _tool("search_services", CatalogClient),
    "get_service": _tool("get_service", CatalogClient),
    "run_service": run_service,
    "estimate_price": estimate_price,
    "get_job": _tool("get_job", JobsClient),
    "list_files": _tool("list_files", FilesClient),
    "get_file": _tool("get_file", FilesClient),
    "get_storage_usage": _tool("get_storage_usage", FilesClient),
    "update_file": _tool("update_file", FilesClient),
    "delete_file": _tool("delete_file", FilesClient),
}

TOOLS: tuple[Callable, ...] = tuple(REGISTRY.values())


_SERVICE_LIST_KEYS = ("id", "name", "display_name", "short_desc", "categories", "is_official", "n_usages")


def _slim_service(item: Any) -> Any:
    """Keep search hits small enough to survive the 2k tool-result cap."""
    if not isinstance(item, dict):
        return item
    return {key: item[key] for key in _SERVICE_LIST_KEYS if key in item}
