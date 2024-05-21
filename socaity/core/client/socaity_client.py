from typing import Union

from socaity.core.job.job import Job
from socaity.core.client.openapi_client import OpenAPIClient, web_request
from socaity.core.endpoint import SocaityEndPoint

from socaity.core.job.job_declarations import JobStatus
from socaity.core.job.socaity_job_result import SocaityJobResult, JobResultFactory


class SocaityClient(OpenAPIClient):

    def __init__(self, endpoint: SocaityEndPoint):
        super().__init__(endpoint)

    def refresh_job_status(self, job: Job) -> Union[SocaityJobResult, str]:
        """
        Refresh the status of the job.
        :param job: the job to refresh
        """
        url = f"{self.endpoint.service_url}/api/job"
        res, error = web_request(url=url, get_params={"job_id": job.result.id})

        if error:
            job.status = JobStatus.FAILED
            raise Exception(error)

        return JobResultFactory.job_result_from_request_response(res)


    def request(self, job: Job) -> Union[dict, bytes, str, object, None]:
        """
        Contrary to the openAPI client, with multiple requests, the job is updated instead of waiting for the response.
        This is an job_id status system similar to runpod / replicate.
        :param job: the job with the payload to send
        :return: the result of the request to the remote API
        """
        if job.result is None or not type(job.result) is SocaityJobResult:
            return super().request(job)

        if job.result._internal_job_id is not None:
            return self.refresh_job_status(job)
