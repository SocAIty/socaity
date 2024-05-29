from socaity.new_registry import Registry
from socaity.new_registry.definitions.model import AIModel
from socaity.new_registry.definitions.endpoint import EndPoint


class Service:
    def __init__(self, service_url: str, model: AIModel = None):
        self.service_url = service_url
        self.model = model if model is not None else AIModel()
        self.endpoints = {}

        # Add the service to the global registry
        Registry.add_service(self)

    def add_endpoint(self, endpoint: EndPoint):
        self.endpoints[endpoint.endpoint_route] = endpoint

    def remove_endpoint(self, endpoint_route: str):
        self.endpoints.pop(endpoint_route, None)
