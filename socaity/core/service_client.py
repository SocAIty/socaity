import functools
from typing import Union

from socaity.core.client.new_client_factory import create_client
from socaity.core.job.async_server_job import AsyncServerJob
from socaity.core.job.job_queue import JobQueue
from socaity.new_registry.definitions.endpoint import EndPoint
from socaity.new_registry.definitions.enums import EndpointSpecification, ModelTag
from socaity.core.job.job import Job
from socaity.new_registry.definitions.model import AIModel
from socaity.new_registry.definitions.service import Service
from socaity.utils.utils import get_function_parameters_as_dict


class ServiceClientAPI:
    """
    With a ServiceClient one specifies the connection to a service and it's endpoints.
    The class provides decorators to register functions that define web endpoints and the post/preprocessing logic.
    Usage:
    - Create a ServiceClient myServiceClient = ServiceClient(service_url="http://service.com/api/my_service")
    - Register endpoints with the @myServiceClient.endpoint decorator.
        - Use the func_type parameter to specify if the function is a preprocess or postprocess function.
            - An preprocess function is the function that is executed before the job is created.

    Calling the methods registered with the endpoint decorator will create a job and add it to the job queue.
    The job queue then executes the job with the given request function.

    Parameters:
    - service_url: The url of the service. E.g. "http://service.com/api/my_service"
    - endpoint_specification: Used to preset how the endpoint is called. Is it just an openapi endpoint
        or does it allow job management like socaity endpoints.
    - model_name: Used to find it in the registry. E.g. "text2speech"
    - model_domain_tags: Used organize the registry and api. E.g. "audio", "image", "text"
    - model_tags: More fine-grained tags for functionality.
    """
    def __init__(
            self,
            # required information for execution
            service_url: str = None,
            endpoint_specification: Union[EndpointSpecification, str] = EndpointSpecification.SOCAITY,
            # optional information for documentation and services
            model_name: str = "new_model",
            model_domain_tags: Union[ModelTag, str] = ModelTag.OTHER,
            model_tags: Union[ModelTag, str] = ModelTag.OTHER,
            *args,
            **kwargs
    ):
        # definitions and registry
        model = AIModel(model_name=model_name, model_domain_tags=model_domain_tags, model_tags=model_tags)
        self.service = Service(service_url=service_url, model=model)
        self.endpoint_specification = endpoint_specification  # is used in the endpoint_decorator as default value

        # The job queue manages jobs and executes them. It's a singleton.
        self.job_queue = JobQueue()
        # registered functions dict with structure: {function_name: JobCallable}
        self._registered_functions = {}
        # registered post process functions dict with structure: {function_name: function}
        self._post_process_functions = {}

    def _endpoint_decorator(
            self,
            func: callable,
            endpoint_route: str = None,
            endpoint_specification: Union[EndpointSpecification, str] = None,
            timeout: int = 3600
    ):
        # add the endpoint to the service
        if endpoint_route is None:
            endpoint_route = func.__name__

        if endpoint_specification is None:
            endpoint_specification = self.endpoint_specification

        endpoint = EndPoint(
            endpoint_route=endpoint_route,
            endpoint_specification=endpoint_specification,
            timeout=timeout
        )
        self.service.add_endpoint(endpoint)

        #
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Union[Job, AsyncServerJob]:
            """
            The wrapper function creates a job and adds it to the job queue.
            """
            # check if there's a post_process_func registered for the function
            post_process_func = self._post_process_functions.get(func.__name__, None)

            # create a request function (the function that sends the web request)
            request_handler = create_client(service=self.service, endpoint=endpoint)

            # parse args, kwargs to parameters for the request
            _kwargs = get_function_parameters_as_dict(func, locals(), kwargs)

            # create a job with the given parameters
            job = self.job_queue.create_job(
                request_func=request_handler.request,
                pre_process_func=func,
                post_process_func=post_process_func,
                refresh_job_status_func=request_handler.refresh_job_status if hasattr(request_handler, "refresh_job_status") else None,
                timeout=3600,
                **_kwargs
            )
            # add job to the job queue and run it
            return self.job_queue.add_job(job)

        return wrapper

    def endpoint(
            self,
            endpoint_route: str = None,
            endpoint_specification: Union[EndpointSpecification, str] = None,
            func_type: str = "preprocess",
            timeout: int = 3600
    ):
        """
        Use @client.endpoint to register a function for execution on an endpoint.
        :param func: The function to be executed.
        :param endpoint_route: The route of the endpoint. E.g. "text2voice" for "service_url/text2voice"
        """
        def decorator(func: callable):
            if func_type == "postprocess":
                self._registered_functions[func.__name__] = func
                return func

            @functools.wraps(func)
            def pre_process_wrapper(func):
                endpoint_decorated_func = self._endpoint_decorator(
                    func=func,
                    endpoint_route=endpoint_route,
                    endpoint_specification=endpoint_specification,
                    timeout=timeout
                )
                return endpoint_decorated_func

            return pre_process_wrapper

        return decorator

    def prepare_params(
            self,
            endpoint_route: str = None,
            endpoint_specification: Union[EndpointSpecification, str] = None,
            timeout: int = 3600
    ):
        return self.endpoint(endpoint_route=endpoint_route,
                             endpoint_specification=endpoint_specification,
                             func_type="preprocess", timeout=timeout)

    def endpoint_post_process(self, endpoint_route: str = None):
        return self.endpoint(endpoint_route=endpoint_route,
                             endpoint_specification=endpoint_specification,
                             func_type="postprocess")


    def __call__(self, **kwargs) -> Union[Job, AsyncServerJob, None]:
        """
        The call function is the default method that will be executed with the client api.
        If not overwritten, we will take the first function that was registered with the client api.

        Subclass this method if you want type hinting. But don't forget to call the endpoint function for execution.
        :kwargs: The parameters for running the job. Note only named are further passed to the job. Transform args to kwargs
        """
        # The parameters for running the job are in *args and **kwargs and then stored in the job itself.
        if len(self._registered_functions) == 0:
            raise ValueError("No function registered with the client api. "
                             "Use @client.endpoint decorator to register a function.")

        func = next(iter(self._registered_functions.values()))
        return func(**kwargs)

