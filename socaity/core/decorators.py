from socaity.core.ClientFactory import create_client
from typing import Union

from socaity.globals import ModelType, EndPointType





class ClientAPI(object):
    """
    This decorator is used to simplify the usage of the API.
    To add a new api to api.py one simply writes
    @ClientAPI(model_name="mymodel")
    def my_model(pyparams, *args, **kwargs):
        ...
    """

    def __init__(self,
            func,
            model_type: Union[ModelType, str, None] = None,
            model_name: str = None,
            endpoint_type: Union[EndPointType, str] = EndPointType.REMOTE,
            provider: str = "socaity",
    ):
        self.func = func
        self.client = create_client(model_type=model_type,
                                    model_name=model_name,
                                    endpoint_type=endpoint_type,
                                    provider=provider)

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            return self.client.run(*args, **kwargs)
        return wrapper