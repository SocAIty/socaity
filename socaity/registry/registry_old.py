"""
The registry is used to list available models and available endpoints.
It provides methods to easily get these.
"""


from typing import Union
from socaity.globals import EndPointType, ModelType
from socaity.registry.endpoints import Endpoints
from socaity.core.Endpoint import LocalEndPoint, RemoteEndPoint


def get_model_type_by_model_name(model_name: str) -> Union[ModelType, None]:
    """
    Get the model type by the model name.
    :param model_name: for example "bark"
    :return: the model type
    """
    for model_type, models in Endpoints.items():
        for model in models:
            if "model_name" in model and model["model_name"].lower() == model_name.lower():
                return model_type
    return None


def filter_endpoints_by_type_and_name(model_type: ModelType, model_name: str):
    """
    Get the model endpoint with a specific model type and model name.
    :param model_type: the model type to filter for
    :param model_name: name of the model to filter for
    :return: endpoint definition
    """
    models = [model for model in Endpoints[model_type] if "model_name" in model and model["model_name"] == model_name]
    if len(models) == 0:
        print(f"Model {model_name} not found in the registry. Taking the first available model instead.")
        return [Endpoints[model_type][0]]
    return models


def get_endpoint(
    model_type: Union[ModelType, str] = None,
    model_name: str = None,
    endpoint_type: Union[EndPointType, str] = EndPointType.REMOTE,
    provider: str = "socaity"
) -> Union[LocalEndPoint, RemoteEndPoint, SOCAITY_ENDPOINT]:
    """
    Get an endpoint from the registry.
    :param model_type: if not provided, it will be inferred from the model_name
    :param model_name: if not provided, the first available model for the model_type will be taken.
    :param endpoint_type: where the model is hosted (local, remote, decentralized).
    :param provider: for example socaity, singularitynet, openai, etc.
    :return: an instance of the endpoint class
    """

    # TODO: improve code and replace all of this with filter methods for lists and dicts.
    # means iterating the dict by a number of values provided as args and filtering / defaulting the dict by these.
    # or: make the list of dicts in the registry a flat list and filter it with a list comprehension.

    ##### DEFAULTING PARAMETERS #####
    # get the model type from the model name if not provided.
    if model_type is None and model_name is not None:
        model_type = get_model_type_by_model_name(model_name)

    if model_type is None:
        raise ValueError(f"Model with name {model_name} not found in the registry.")

    # get the default model if model_type is provided but model_name is not
    if model_type is not None and model_name is None:
        model_name = Endpoints[model_type][0]["model_name"]
        print(f"Model name not provided. Defaulting to {model_name}.")

    # get the endpoint_type from the string if provided or default
    if isinstance(endpoint_type, str) and endpoint_type in EndPointType._value2member_map_:
        endpoint_type = EndPointType(endpoint_type)
    else:
        print(f"Endpoint type {endpoint_type} not found for model {model_name} in the registry. Defaulting to remote.")
        endpoint_type = EndPointType.REMOTE

    provider = provider.lower() if isinstance(provider, str) else "socaity"

    #### FILTERING ENDPOINTS ####

    # filter the endpoints with the specified model type and name
    model_endpoints = filter_endpoints_by_type_and_name(model_type, model_name)

    # filter the endpoints with the specified endpoint type
    model_endpoints = [endpoint for endpoint in model_endpoints if endpoint_type in endpoint]

    # filter the endpoints with the specified provider
    model_endpoints = [endpoint for endpoint in model_endpoints if "provider" in endpoint and provider == endpoint["provider"]]
    if len(model_endpoints) == 0:
        raise ValueError(f"Couldn't find any endpoints for model {model_name} with type {model_type} and provider {provider}.")

    filtered_endpoint = model_endpoints[0]

    # instantiate endpoint class with the endpoint definition
    kwargs = { "model_type": model_type, "model_name": model_name, "endpoint_type": endpoint_type }
    if endpoint_type == EndPointType.LOCAL:


        return LocalEndPoint(model_type=model_type, model_name=model_name, api_url=)
    elif endpoint_type == EndPointType.REMOTE:
        return RemoteEndPoint()
    else:
        print(f"Endpoint type {endpoint_type} not supported. Defaulting to socAIty.")
        return SOCAITY_ENDPOINT(endpoint_def=model_name)




