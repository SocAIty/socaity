from typing import Union
from socaity.globals import EndPointType, ModelType
from socaity.registry.endpoints import Endpoints
from socaity.core.endpoint import LocalEndPoint, RemoteEndPoint, EndPoint


class ActiveClientRegistry:
    """
    This class stores the clients created. This is done to avoid creating multiple clients for the same model.
    """
    def __init__(self):
        self.ACTIVE_CLIENTS = {}

    def add_active_client(self, client):
        self.ACTIVE_CLIENTS[str(client.endpoint)] = client

    def get_client(self, endpoint: EndPoint, default_return_value=None):
        return self.ACTIVE_CLIENTS.get(str(endpoint), default_return_value)

    def remove_client(self, name: str):
        self.ACTIVE_CLIENTS.pop(name, None)


ACTIVE_CLIENT_REGISTRY = ActiveClientRegistry()


def get_endpoint(
    model_type: Union[ModelType, str] = None,
    model_name: str = None,
    endpoint_type: Union[EndPointType, str] = EndPointType.REMOTE,
    provider: Union[str, None] = "socaity"
) -> Union[LocalEndPoint, RemoteEndPoint]:
    """
    Get an endpoint to connect to a model hosted on a provider (Remote, Local or Decentralized).
    :param model_type: for example "text2speech"
    :param model_name: for example "bark"
    :param endpoint_type: for example "remote"
    :param provider: for example "socaity"
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
        print(f"No model_name provided. Defaulting to first available model: {model_name}")
        return get_endpoint(model_type=model_type, model_name=model_name, endpoint_type=endpoint_type, provider=provider)

    # filter endpoints by endpoint_type
    endpoint_type = EndPointType(endpoint_type) if isinstance(endpoint_type, str) else endpoint_type
    filtered_endpoints = [endpoint for endpoint in filtered_endpoints if endpoint.endpoint_type == endpoint_type]
    if len(filtered_endpoints) == 0:
        raise ValueError(f"No endpoint found with model_type {model_type} and endpoint_type {endpoint_type}.")

    # filter endpoints by provider
    if provider is not None:
        provider = provider.lower()
        filtered_endpoints = [
            endpoint for endpoint in filtered_endpoints
            if endpoint.provider is not None and endpoint.provider.lower() == provider
        ]
        if len(filtered_endpoints) == 0:
            print(f"Provider {provider} for model {model_name} not found. Defaulting to any.")
            return get_endpoint(model_type=model_type,
                                    model_name=model_name,
                                    endpoint_type=EndPointType.REMOTE,
                                    provider=None)
    # return the first endpoint
    return filtered_endpoints[0]
