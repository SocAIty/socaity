from typing import Union

from socaity.core.client.local_client import LocalClient
from socaity.core.client.remote_client import RemoteClient
from socaity.globals import ModelType, EndPointType
from socaity.registry.registry import get_endpoint, ACTIVE_CLIENT_REGISTRY


def create_client(
        model_type: Union[ModelType, str, None] = None,
        model_name: str = None,
        endpoint_type:  Union[EndPointType, str] = EndPointType.REMOTE,
        provider: str = "socaity",
) -> Union[LocalClient, RemoteClient]:
    """
    Create a client to interact with an API.
    :param model_type: for example "text2speech"
    :param model_name: for example "bark"
    :param endpoint_type: for example "remote"
    :param provider: for example "socaity"
    :return: a client to interact with the API
    """
    clients = {
        EndPointType.LOCAL: LocalClient,
        EndPointType.REMOTE: RemoteClient
    }

    endpoint = get_endpoint(model_type=model_type, model_name=model_name, endpoint_type=endpoint_type, provider=provider)

    # check if the client is already created and return from the registry if it is the case
    client = ACTIVE_CLIENT_REGISTRY.get_client(endpoint, default_return_value=None)
    if client is not None:
        return client


    # create a new client
    if endpoint.endpoint_type in clients:
        client = clients[endpoint.endpoint_type](endpoint)
    else:
        print(f"Endpoint type {endpoint_type} not supported. Defaulting to remote.")
        client = RemoteClient(endpoint)

    # add the client to the registry
    ACTIVE_CLIENT_REGISTRY.add_active_client(client)

    return client
