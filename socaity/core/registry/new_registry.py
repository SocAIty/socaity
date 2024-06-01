
from typing import Union
from singleton_decorator import singleton
from socaity.new_registry.definitions.service import Service

#from socaity.new_registry.definitions.enums import EndpointSpecification, ModelTag


@singleton
class _Registry:
    """
    The registry is used to organize services, endpoints and models.

    Service: (e.g. socaity.com/api/face2face)
        Endpoint_1: (e.g. socaity.com/api/face2face/predict)
        Endpoint_2: (e.g. socaity.com/api/face2face/swap_from_reference)

    This makes it easy to list and find services, endpoints and models.
    """
    def __init__(self):
        self.services = {}

    def add_service_client(self, service: ServiceClient):
        self.services[service.service_url] = service

    def get_service(self, service_url: str):
        return self.services.get(service_url)

    #def add_endpoint(
    #        self,
    #        service_url: str,
    #        endpoint_route: str,
    #        endpoint_specification: Union[EndpointSpecification, str] = EndpointSpecification.SOCAITY,
    #        model_type: ModelTag = Union[ModelTag.ANY],
    #        model_name: str = None
    #):
    #    pass





