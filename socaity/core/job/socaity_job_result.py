"""
This is a copy of the socaity_router job_result file and JobStatus file.
It mirrors the data structure of the job result object of socaity_router.
If the result of an endpoint is this structure, the client_api assumes it is interacting with an socaity endpoint.
On that way, we can queue, wait and get the result of the job.
"""
from dataclasses import dataclass
from typing import Optional, Union

from socaity.core.job.job_declarations import SocaityServerJobStatus


@dataclass
class SocaityJobResult:
    """
    When the user (client) sends a request to an Endpoint, a ClientJob is created.
    This job contains the information about the request and the response.
    """
    id: str
    status: SocaityServerJobStatus
    progress: Optional[float] = 0.0
    message: Optional[str] = None
    result: Optional[object] = None

    created_at: Optional[str] = None
    queued_at: Optional[str] = None
    execution_started_at: Optional[str] = None
    execution_finished_at: Optional[str] = None

    endpoint_protocol: Optional[str] = "socaity"


class JobResultFactory:
    @staticmethod
    def job_result_from_request_response(request_response: dict) -> Union[SocaityJobResult, object]:

        # was an endpoint that returned type socait_job_result
        required_fields = ['id', 'status']
        if all(field in request_response for field in required_fields):
            request_response['status'] = SocaityServerJobStatus(request_response['status'])
            return SocaityJobResult(**request_response)

        # any other endpoint
        return request_response
