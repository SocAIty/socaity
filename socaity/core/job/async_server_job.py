from datetime import datetime

from socaity.core.job.job import Job
from socaity.core.job.job_declarations import JobStatus, SocaityServerJobStatus
from socaity.core.job.socaity_job_result import JobResultFactory


class AsyncServerJob(Job):
    """
    A job that is executed on a server that returns a job_id and the job has to be fetched until it is finished.
    """
    def __init__(
            self,
            request_func: callable,
            refresh_func: callable,  # required to refresh job status on server
            pre_process_func: callable = None,
            post_process_func: callable = None,
            timeout: int = 3600,  # seconds to stay in queue before deleted
            **kwargs
        ):
        super().__init__(
            pre_process_func=pre_process_func,
            post_process_func=post_process_func,
            request_func=request_func,
            timeout=timeout,
            **kwargs
        )
        self._refresh_func = refresh_func

    def server_ended_job(self) -> bool:
        if self.result is None:
            return False

        # job status from server
        return self.result.status in [
            SocaityServerJobStatus.FINISHED,
            SocaityServerJobStatus.FAILED,
            SocaityServerJobStatus.TIMEOUT
        ]

    def refresh_job_status(self):
        # make request to server to update job status
        try:
            self.result = self._refresh_func(self)
            self.job_statistics.last_status_update_at = datetime.utcnow()

            if self.server_ended_job():
                self.job_statistics.request_result_received_at = datetime.utcnow()
                self.status = JobStatus.JOB_RESULT_RECEIVED

        except Exception as e:
            self.status = JobStatus.FAILED
            self.error_msg = str(e)
        return self

    def request(self):
        self.job_statistics.request_send_at = datetime.utcnow()
        try:
            result = self._request_func(self)
            self.result = JobResultFactory.job_result_from_request_response(result)
        except Exception as e:
            self.status = JobStatus.FAILED
            self.error_msg = str(e)
        return self
