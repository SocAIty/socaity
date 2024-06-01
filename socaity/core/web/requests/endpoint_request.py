from socaity.core.jobs.async_jobs.async_job import AsyncJob
from socaity.core.web.definitions.endpoint import EndPoint
from socaity.core.web.definitions.socaity_server_response import SocaityServerResponse, SocaityServerJobStatus
from socaity.core.web.requests.request_handler import RequestHandler
from socaity.core.web.requests.server_response_parser import parse_response
import time

class EndPointRequest:
    """
    Some endpoints are async_jobs and return a job id. Others are sync and return the result directly.
    Based on the first request response, the class decides with what kind of endpoint it is interacting with.

    In case of a sync job endpoint, the result is returned directly.
    In case of an async_jobs job endpoint like the ones that implement the socaity protocol:
        1. The class automatically refreshes the job until it's finished.
        -  The class sends requests to the refresh status url until the job is finished.
        -  To do so, it submits more async_jobs requests with callbacks with the request handler.
    """
    def __init__(
            self,
            endpoint: EndPoint,
            request_handler: RequestHandler,
            refresh_interval: float = None
    ):
        self._endpoint = endpoint
        self._request_handler = request_handler
        self._refresh_interval = refresh_interval

        # public attributes to get the result
        self.result = None
        self.in_between_result = None

    def request(self, *args, **kwargs):
        # schedule the first async_jobs job
        return self._request_handler.request_endpoint_async(
            self._endpoint,
            callback=self._response_callback,
            *args,
            **kwargs
        )


    def wait_until_finished(self):
        """
        This function waits until the job is finished and returns the result.
        :return:
        """
        while self.result is None:
            time.sleep(0.1)
        return self.result

    def _response_callback(self, async_job: AsyncJob):
        """
        This function is called when the first async_jobs job is finished.
        It checks if the result is a socaity job result and sets the status accordingly.
        :param future: the future object of the async_jobs job
        :return:
        """
        job_result = parse_response(async_job.result)
        # if not is a socaity job, we can return the result
        if not isinstance(job_result, SocaityServerResponse):
            self.result = job_result
            return self.result
        # check if socaity job is finished
        if job_result.status == SocaityServerJobStatus.FINISHED:
            self.in_between_result = None
            self.result = job_result

            return self.result

        self.in_between_result = job_result
        # if not finished, we need to refresh the job
        refresh_url = self._request_handler.service_url + job_result.refresh_job_url

        # by calling this recursively we can refresh the job until it's finished
        self._request_handler.request_url_async(
            refresh_url,
            callback=self._response_callback,
            delay=self._refresh_interval
        )