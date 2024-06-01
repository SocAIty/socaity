from typing import Union

from socaity.core.web.service_client import ServiceClient


class _ServiceClientAPI:
    """
    The ServiceClient API uses the service client to perform various tasks.
    1. It uses the service client to make requests to the service.
        - It understands the types of the response like socaity job results.
        - In case of a socaity job subsequent requests are made to the service until the final result is retrieved.
    2. It can batch requests.
    3. It makes writing sdk classes easier.
    """

    def __init__(self, service_name: str, service_url: str):
        self.service_client = registry.get_service(service_name_or_service_client)


    def request(self, endpoint_route: str, *args, **kwargs):
        async_job = self.service_client(endpoint_route=endpoint_route, call_async=True, *args, **kwargs)
        # Wrap async_jobs job in other object with additional functions like wait for result
        # This is also an async_jobs job and is submitted to the async_jobs job manager
        return SocaityRequest(async_job)



def job_decorator(queue_size: int = 100):
    """
    The job decorator is used to create an internal job that is added to the job queue.
    The job is processed threaded and the job state is updated.
    """
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            self.request = _job_request(job_id, self.request)

            # create a job and add it to the job manager
            job = Job(func, *args, **kwargs)
            job_manager.add_job(job)
            return job

        return wrapper

    return decorator




def ServiceClientAPI(service_name_or_service_client: Union[str, ServiceClient]):
    """
    The ServiceClientAPI decorator is used to create a new service client api.
    The service client api is used to create internal jobs and manage them.
    """
    def decorator(cls):
        # search the service in the registry or add id directly to class
        service_client = service_name_or_service_client
        if isinstance(service_name_or_service_client, str):
            service_client = registry.get_service(service_name_or_service_client)

        # Instantiate a real ServiceClientAPI and add the wrapped class to it
        service_client_api = _ServiceClientAPI(cls)

        # create a request wrapper that accepts the "self" of the class that is wrapped and forwards it.
        def request(self, endpoint_route: str, *args, **kwargs):
            return service_client_api.request(
                class_of_caller=self,
                endpoint_route=endpoint_route,
                call_async=True, *args, **kwargs
            )

        # add the ServiceClientAPI request method to the class
        cls.request = request

        return cls

    return decorator

