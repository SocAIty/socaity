from socaity.globals import EndPointType, ModelType

class EndPoint:
    """
    An endpoint contains the information to connect to a model hosted on a provider (Remote, Local or Decentralized).
    """
    def __init__(
        self,
        model_type: ModelType,
        model_name: str,
        endpoint_type: EndPointType,
        provider: str = None,
        *args,
        **kwargs
    ):
        self.model_name = model_name
        self.model_type = model_type
        self.endpoint_type = endpoint_type
        self.provider = provider


class RemoteEndPoint(EndPoint):
    def __init__(self, model_type: ModelType, model_name: str, api_url: str, *args, **kwargs):
        super().__init__(model_type=model_type, model_name=model_name, endpoint_type=EndPointType.REMOTE, *args, **kwargs)
        self.api_url = api_url


class LocalEndPoint(EndPoint):
    def __init__(self, api_url: str, start_bat_path: str = "", *args, **kwargs):
        super().__init__(endpoint_type=EndPointType.LOCAL, *args, **kwargs)
        self.api_url = api_url
        self.start_bat_path = start_bat_path


class SocaityEndpoint(RemoteEndPoint):
    """ Helper class with predifined URLS to define the SOCAITY endpoints. """
    def __init__(self, model_type: ModelType, model_name: str, *args, **kwargs):
        api_url = f"https://socaity.ai/api/{model_type.value}/{model_name}"
        super().__init__(model_type=model_type, model_name=model_name, api_url=api_url, provider="socaity", *args, **kwargs)