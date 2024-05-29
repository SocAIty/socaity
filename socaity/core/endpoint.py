from typing import Union

from socaity.globals import SOCAITY_API_URL, SOCAITY_API_VERSION
from socaity.new_registry.definitions.enums import EndPointType, EndpointSpecification, ModelTag


class EndPoint:
    """
    An endpoint contains the information to connect to an api.
    """
    def __init__(
            self,
            # descriptors
            model_type: Union[ModelTag, str],
            model_name: str,
            # relevant for for execution
            endpoint_type: Union[EndPointType, str],
            endpoint_name: str = None,
            endpoint_specification: Union[EndpointSpecification, str] = EndpointSpecification.OPENAPI,
            post_params: list = None,
            get_params: list = None,
            files: list = None,
            *args,
            **kwargs
    ):
        """
        :param model_type: The type of the model (for example ModelTag.TEXT2VOICE).
        :param model_name: The name of the model (for example "bark")
        :param endpoint_type: The type of the endpoint (for example EndPointType.REMOTE)
        :param endpoint_specification: The endpoint_specification of the model (for example "socaity")
        :param post_params: The parameters to be sent in the POST request
        :param get_params: The parameters to be sent in the GET request
        :param files: The files to be sent in the request.
        All parameters in a request which are not defined in post, get, or files are default as post parameters.
        """
        self.model_name = model_name
        self.model_type = ModelTag(model_type) if isinstance(model_type, str) else model_type
        self.endpoint_type = EndPointType(endpoint_type) if isinstance(endpoint_type, str) else endpoint_type
        self.endpoint_name = endpoint_name
        self.endpoint_specification = EndpointSpecification(endpoint_specification) \
            if isinstance(endpoint_specification, str) else endpoint_specification

        # initiating empty lists if not given to avoid errors
        self.post_params = post_params if post_params is not None else []
        self.get_params = get_params if get_params is not None else []
        self.files = files if files is not None else []

    def __str__(self):
        return f"{self.model_type.value}_{self.model_name}_{self.endpoint_type.value}_{self.endpoint_specification.value}"


class OpenAPIEndpoint(EndPoint):
    def __init__(self, model_type: ModelTag, model_name: str, service_url: str, endpoint_name: str, *args, **kwargs):
        super().__init__(model_type=model_type, model_name=model_name, endpoint_type=EndPointType.REMOTE,
                         endpoint_name=endpoint_name,
                         *args, **kwargs)
        # remove trailing slash
        self.service_url = service_url if service_url[-1] != "/" else service_url[:-1]
        self.endpoint_name = endpoint_name


class LocalEndPoint(EndPoint):
    def __init__(self, service_url: str, endpoint_name: str, start_bat_path: str = "", *args, **kwargs):
        super().__init__(service_url=service_url, endpoint_name=endpoint_name, endpoint_type=EndPointType.LOCAL,
                         *args, **kwargs)
        self.service_url = service_url if service_url[-1] != "/" else service_url[:-1]
        self.start_bat_path = start_bat_path


class SocaityEndPoint(EndPoint):
    def __init__(self, service_url: str, endpoint_name: str, model_type: ModelTag, model_name: str, *args, **kwargs):
        self.service_url = service_url if service_url[-1] != "/" else service_url[:-1]
        super().__init__(
            model_type=model_type, model_name=model_name,
            service_url=service_url, endpoint_name=endpoint_name,
            endpoint_type=EndPointType.SOCAITY,
            endpoint_specification=EndpointSpecification.SOCAITY,
            *args, **kwargs)


class SocaityServerEndpoint(SocaityEndPoint):
    """ Helper class with predefined URLS to define the SOCAITY endpoints. """
    def __init__(self, model_type: ModelTag, model_name: str, *args, **kwargs):
        self.service_url = f"{SOCAITY_API_URL}/inferapi/genai/{SOCAITY_API_VERSION}/"
        self.endpoint_name = f"{model_type.value}/{model_name}"
        super().__init__(model_type=model_type, model_name=model_name,
                         service_url=self.service_url, endpoint_name=self.endpoint_name,
                         *args, **kwargs)
