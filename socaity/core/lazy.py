"""Lazy relation loading for catalog entities.

List calls return slim objects (sparse fieldsets keep the wire light).
``LazyAIService`` wraps such a slim ``AIService`` and fetches the full record
once a relation (models, endpoints, deployments) is accessed:

    services = socaity.list_services()
    services[0].models   # -> triggers one catalog fetch, then cached
"""
from typing import List

from socaity_schemas.platform import AIService

RELATIONS = ("models", "endpoints", "deployments")


class LazyAIService:
    """Attribute proxy around AIService; relations hydrate on first access."""

    def __init__(self, service: AIService, client):
        object.__setattr__(self, "_service", service)
        object.__setattr__(self, "_client", client)
        object.__setattr__(self, "_hydrated", False)

    def __getattr__(self, item):
        if item in RELATIONS and not self._hydrated and not getattr(self._service, item):
            self._hydrate()
        return getattr(self._service, item)

    def __setattr__(self, key, value):
        setattr(self._service, key, value)

    def _hydrate(self) -> None:
        object.__setattr__(self, "_hydrated", True)
        full = self._client.get_service(self._service.id or self._service.name)
        if full:
            object.__setattr__(self, "_service", full)

    @property
    def raw(self) -> AIService:
        """The underlying (possibly slim) AIService."""
        return self._service

    def __repr__(self):
        return f"LazyAIService({self._service.name or self._service.id})"


def wrap_services(services: List[AIService], client) -> List[LazyAIService]:
    return [LazyAIService(service, client) for service in services]
