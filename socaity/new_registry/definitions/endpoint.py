from typing import Union

from socaity.new_registry.definitions.enums import EndpointSpecification, ModelTag


class EndPoint:
    def __init__(
            self,
            endpoint_route: str,
            endpoint_specification: Union[EndpointSpecification, str] = EndpointSpecification.SOCAITY,
            timeout: int = 3600
    ):
        self.endpoint_route = endpoint_route
        self.endpoint_specification = endpoint_specification
        self.timeout = timeout
