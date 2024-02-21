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
        endpoint_name: str = None,
        provider: str = None,
        post_params: list = None,
        get_params: list = None,
        files: list = None,
        *args,
        **kwargs
    ):
        """
        :param model_type: The type of the model (for example ModelType.TEXT2VOICE)
        :param model_name: The name of the model (for example "bark")
        :param endpoint_type: The type of the endpoint (for example EndPointType.REMOTE)
        :
        :param provider: The provider of the model (for example "socaity")
        :param post_params: The parameters to be sent in the POST request
        :param get_params: The parameters to be sent in the GET request
        :param files: The files to be sent in the request.
        All parameters in a request which are not defined in post, get, or files are default as post parameters.
        """

        self.model_name = model_name
        self.model_type = model_type
        self.endpoint_type = endpoint_type
        self.endpoint_name = endpoint_name
        self.provider = provider

        # initiating empty lists if not given to avoid errors
        self.post_params = post_params if post_params is not None else []
        self.get_params = get_params if get_params is not None else []
        self.files = files if files is not None else []

    def __str__(self):
        return f"{self.model_type.value}_{self.model_name}_{self.endpoint_type.value}_{self.provider}"



class RemoteEndPoint(EndPoint):
    def __init__(self, model_type: ModelType, model_name: str, service_url: str, endpoint_name: str, *args, **kwargs):
        super().__init__(model_type=model_type, model_name=model_name, endpoint_type=EndPointType.REMOTE,
                         endpoint_name=endpoint_name,
                         *args, **kwargs)
        self.service_url = service_url
        self.endpoint_name = endpoint_name


class LocalEndPoint(EndPoint):
    def __init__(self, service_url: str, endpoint_name: str, start_bat_path: str = "", *args, **kwargs):
        super().__init__(service_url=service_url, endpoint_name=endpoint_name, endpoint_type=EndPointType.LOCAL,
                         *args, **kwargs)
        self.service_url = service_url
        self.start_bat_path = start_bat_path


class SocaityEndpoint(RemoteEndPoint):
    """ Helper class with predifined URLS to define the SOCAITY endpoints. """
    def __init__(self, model_type: ModelType, model_name: str, *args, **kwargs):
        self.service_url = f"https://socaity.ai/api/"
        self.endpoint_name = f"{model_type.value}/{model_name}"
        super().__init__(model_type=model_type, model_name=model_name,
                         service_url=self.service_url, endpoint_name=self.endpoint_name,
                         provider="socaity", *args, **kwargs)

