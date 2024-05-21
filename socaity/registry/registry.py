import logging
from typing import Union
from singleton_decorator import singleton

from socaity.globals import EndPointType, ModelType, EndpointSpecification
from socaity.registry.endpoints import Endpoints
from socaity.core.endpoint import LocalEndPoint, OpenAPIEndpoint, EndPoint, SocaityEndPoint
import threading

from socaity.utils.utils import get_function_parameters_as_dict

lock = threading.Lock()


@singleton
class ActiveClientRegistry:
    """
    This class stores the clients created. This is done to avoid creating multiple clients for the same model.
    """

    def __init__(self):
        self.ACTIVE_CLIENTS = {}

    def add_active_client(self, client):
        with lock:
            self.ACTIVE_CLIENTS[str(client.endpoint)] = client

    def get_client(self, endpoint: EndPoint, default_return_value=None):
        with lock:
            return self.ACTIVE_CLIENTS.get(str(endpoint), default_return_value)

    def remove_client(self, name: str):
        with lock:
            self.ACTIVE_CLIENTS.pop(name, None)


ACTIVE_CLIENT_REGISTRY = ActiveClientRegistry()


def get_endpoint(
        model_type: Union[ModelType, str] = None,
        model_name: str = None,
        endpoint_type: Union[EndPointType, str] = EndPointType.REMOTE,
        endpoint_specification: Union[EndpointSpecification, str, None] = EndpointSpecification.SOCAITY
) -> Union[LocalEndPoint, OpenAPIEndpoint]:
    """
    Get an endpoint to connect to a model hosted on a endpoint_specification (Remote, Local or Decentralized).
    :param model_type: for example "text2speech"
    :param model_name: for example "bark"
    :param endpoint_type: for example "remote"
    :param endpoint_specification: for example "socaity"
    :return: an endpoint to connect to the model
    """
    filtered_endpoints = Endpoints
    # filter endpoints by model_type
    if model_type is not None:
        model_type = ModelType(model_type) if isinstance(endpoint_type, str) else model_type
        filtered_endpoints = [endpoint for endpoint in filtered_endpoints if endpoint.model_type == model_type]

    # filter endpoints by model_name
    if model_name is not None:
        filtered_endpoints = [endpoint for endpoint in filtered_endpoints if endpoint.model_name == model_name]
    else:
        model_name = filtered_endpoints[0].model_name
        logging.info(f"No model_name provided. Defaulting to first available model: {model_name}")
        return get_endpoint(model_type=model_type, model_name=model_name, endpoint_type=endpoint_type,
                            endpoint_specification=endpoint_specification)

    # filter endpoints by endpoint_type
    endpoint_type = EndPointType(endpoint_type) if isinstance(endpoint_type, str) else endpoint_type
    filtered_endpoints = [endpoint for endpoint in filtered_endpoints if endpoint.endpoint_type == endpoint_type]
    if len(filtered_endpoints) == 0:
        raise ValueError(f"No endpoint found with model_type {model_type} and endpoint_type {endpoint_type}.")

    # filter endpoints by endpoint_specification
    if endpoint_specification is not None:
        endpoint_specification = EndpointSpecification(endpoint_specification) if isinstance(endpoint_specification, str) else endpoint_specification

        filtered_endpoints = [
            endpoint for endpoint in filtered_endpoints
            if endpoint.endpoint_specification is not None and endpoint.endpoint_specification == endpoint_specification
        ]
        if len(filtered_endpoints) == 0:
            logging.info(f"Provider {endpoint_specification} for model {model_name} not found. Defaulting to any.")
            return get_endpoint(
                model_type=model_type,
                model_name=model_name,
                endpoint_type=endpoint_type,
                endpoint_specification=None
            )
    # return the first endpoint
    return filtered_endpoints[0]


def add_endpoint(endpoint: EndPoint):
    """
    Add an endpoint to the registry on the fly.
    :param endpoint: the endpoint to add
    """
    Endpoints.append(endpoint)
    logging.info(f"Endpoint {endpoint} added to the registry.")


def add_openapi_endpoint(
        service_url: str,
        endpoint_name: str,
        endpoint_specification: EndpointSpecification = EndpointSpecification.SOCAITY,
        model_type: ModelType = ModelType.ANY,
        model_name: str = "new_model",
        *args, **kwargs
    ):
    """
    Add a remote endpoint to the registry on the fly.
    For example service_url = "http://localhost:8009" and endpoint_name = "text2voice"
    results in "http://localhost:8009/text2voice"
    :param service_url: the url of the service
    :param endpoint_name: the name of the endpoint.
    :param endpoint_specification: the endpoint_specification of the model (for example "socaity", "openapi")
    """
    _kwargs = get_function_parameters_as_dict(add_openapi_endpoint, locals(), kwargs)
    add_endpoint(OpenAPIEndpoint(**_kwargs))


def add_socaity_endpoint(service_url: str, endpoint_name: str,
                         model_type: ModelType = ModelType.ANY,
                         model_name: str = "socaity_model", *args, **kwargs):
    _kwargs = get_function_parameters_as_dict(add_socaity_endpoint, locals(), kwargs)
    add_endpoint(SocaityEndPoint(**_kwargs))


def add_local_endpoint(service_url: str, endpoint_name: str, start_bat_path: str = "", *args, **kwargs):
    _kwargs = get_function_parameters_as_dict(add_local_endpoint, locals(), kwargs)
    add_endpoint(LocalEndPoint(**_kwargs))

