from socaity.core import OpenAPIClient
from socaity.core.client.socaity_client import SocaityClient
from socaity.new_registry.definitions.endpoint import EndPoint, EndpointSpecification
from socaity.new_registry.definitions.service import Service


def create_client(service: Service, endpoint: EndPoint):
    """
    Create a client for the given service and endpoint.
    """

    clients = {
        EndpointSpecification.OPENAPI: OpenAPIClient,
        EndpointSpecification.SOCAITY: SocaityClient
    }

    cl_class = OpenAPIClient # default client class
    if endpoint.endpoint_specification in clients:
        cl_class = clients[endpoint.endpoint_specification]

    client = cl_class(service, endpoint)

    return client