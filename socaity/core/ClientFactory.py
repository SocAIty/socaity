from typing import Union

from socaity.core.Client import LocalClient, RemoteClient
from socaity.globals import ModelType, EndPointType
from socaity.registry.registry import get_endpoint


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
    if endpoint.endpoint_type in clients:
        return clients[endpoint.endpoint_type](endpoint)
    else:
        print(f"Endpoint type {endpoint_type} not supported. Defaulting to remote.")
        return RemoteClient(endpoint)

