import httpx
from socaity.core.web.definitions.endpoint import EndPoint
from socaity.core.jobs.async_jobs.async_job import AsyncJob
from socaity.core.jobs.async_jobs.async_job_manager import AsyncJobManager


class RequestHandler:
    """
    The request handler is an interface between async jobs and web requests.
    1. Requests to endpoints are implemented as coroutines.
    2. It submits those request coroutines to the AsyncJobManager; where they are executed asynchronously.
    It also implements the logic to prepare the parameters for the request.
    """

    def __init__(self, service_url: str, async_job_manager: AsyncJobManager = None):
        self.service_url = service_url
        # add the async_jobs job manager or create a new one
        self.async_job_manager = async_job_manager if async_job_manager is not None else AsyncJobManager()

    def request_endpoint_sync(self, endpoint: EndPoint, *args, **kwargs):
        job = self.request_endpoint_async(endpoint, *args, **kwargs)
        return job.result()

    def request_endpoint_async(self, endpoint: EndPoint, callback: callable = None, *args, **kwargs) -> AsyncJob:
        """
        Makes a request to an endpoint.
        :param endpoint: The endpoint to make the request to.
        :param callback: The callback function to call when the request is done.
        :param args: The arguments to pass to the request.
        :param kwargs: The keyword arguments to pass to the request.
        :return: The response of the request.
        """
        get_p, post_p, file_p, header_p = self._prepare_endpoint_params_for_request(endpoint, *args, **kwargs)

        return self.request_url_async(
            url=f"{self.service_url}/{endpoint.endpoint_route}",
            get_params=get_p,
            post_params=post_p,
            files=file_p,
            headers=header_p,
            callback=callback
        )

    def request_url_async(
            self,
            url: str,
            get_params: dict = None,
            post_params: dict = None,
            headers: dict = None,
            files: dict = None,
            callback: callable = None,
            delay: float = None
    ) -> AsyncJob:
        """
        Makes a request to the given url.
        :param url: The url of the request.
        :param get_params: The parameters to be sent in the GET request.
        :param post_params: The parameters to be sent in the POST request.
        :param headers: The header_params of the request.
        :param files: The files to be sent in the request.
        :param callback: The callback function to call when the request is done.
        :param delay: The delay in seconds before the request is made.
        :return: The response of the request as an async_jobs job.
        """
        req_coroutine = self.request(url, get_params, post_params, headers, files)

        async_job = self.async_job_manager.submit(req_coroutine, callback=callback, delay=delay)
        return async_job

    @staticmethod
    def _prepare_endpoint_params_for_request(endpoint: EndPoint, *args, **kwargs):
        # make dict from args and kwargs
        _named_args = {k: v for k, v in locals().items() if k in endpoint.params()}
        _named_args.update(kwargs)

        # sort the parameters by paramater typ
        get_params = {k: v for k, v in _named_args.items() if k in endpoint.get_params}
        post_params = {k: v for k, v in _named_args.items() if k in endpoint.post_params}
        file_params = {k: v for k, v in _named_args.items() if k in endpoint.file_params}
        header_params = {k: v for k, v in _named_args.items() if k in endpoint.headers}

        return get_params, post_params, file_params, header_params


    @staticmethod
    def add_get_params_to_url(url: str, get_params: dict):
        """
        Adds the get parameters to the url.
        :param url: The url to add the parameters to.
        :param get_params: The parameters to add.
        :return: The url with the parameters added.
        """
        if get_params:
            url += "?"
            for k, v in get_params.items():
                url += f"{k}={v}&"
            url = url[:-1]
        return url

    @staticmethod
    async def request(url: str = None, get_params=None, post_params=None, headers=None, files=None):
        """
        Makes a request to the given url.
        :param get_params: The parameters to be sent in the GET request.
        :param post_params: The parameters to be sent in the POST request.
        :param url: The url of the request.
        :param headers: The header_params of the request.
        :param files: The files to be sent in the request.
        :return: The response of the request.
        """
        url = RequestHandler.add_get_params_to_url(url, get_params)
        async with httpx.AsyncClient() as client:
            return await client.post(url, params=post_params, files=files, headers=headers)

