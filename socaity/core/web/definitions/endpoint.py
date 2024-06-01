from typing import Union

from socaity.core.definitions.enums import EndpointSpecification


class EndPoint:
    def __init__(
            self,
            endpoint_route: str,
            endpoint_specification: Union[EndpointSpecification, str] = EndpointSpecification.SOCAITY,
            get_params: dict = None,
            post_params: dict = None,
            file_params: dict = None,
            header_params: dict = None,
            timeout: float = 3600
    ):
        """

        :param endpoint_route:
        :param endpoint_specification: determines how the endpoint is called. For example socaity endpoints use jobs.
        :param get_params: Defines the parameters which are send as url?params=... to the endpoint.
            It is a dict in format {param_name: param_type} for example {"my_text": str}.
        :param post_params: Defines the parameters which are send as post parameters.
            Expects a dict in format {param_name: param_type} for example {"my_text": str}
        :param file_params:
        :param timeout: time until the request fails.
        """

        # remove slash at beginning
        self.endpoint_route = endpoint_route if endpoint_route[0] != "/" else endpoint_route[1:]
        self.endpoint_specification = endpoint_specification
        self.timeout = timeout
        self.get_params = get_params if get_params is not None else {}
        self.post_params = post_params if post_params is not None else {}
        self.file_params = file_params if file_params is not None else {}
        self.headers = header_params if header_params is not None else {}

    def params(self):
        all_params = { k: v for k,v in self.get_params.items() }
        all_params.update(self.post_params)
        all_params.update(self.file_params)
        return all_params


def create_endpoint(
        endpoint_route: str,
        endpoint_specification: Union[EndpointSpecification, str] = EndpointSpecification.SOCAITY,
        timeout: int = 3600
):
    return EndPoint(
        endpoint_route=endpoint_route,
        endpoint_specification=endpoint_specification,
        timeout=timeout)


def create_socaity_endpoint(endpoint_route: str, timeout: int = 3600):
    return create_endpoint(
        endpoint_route=endpoint_route,
        endpoint_specification=EndpointSpecification.SOCAITY,
        timeout=timeout
    )