from datetime import datetime, timedelta
from uuid import uuid4

from socaity.core.job.job_declarations import JobStatistics, JobStatus


class Job:
    """
    A job contains the:
     - the payload to handle a request.
     - references to the pre and post processing functions.
     - the result of the request.
     - the statistics and execution times of the job.
    """
    def __init__(
            self,
            pre_process_func: callable = None,
            post_process_func: callable = None,
            request_func: callable = None,
            timeout: int = 3600,  # seconds to stay in queue before deleted
            **kwargs
        ):
        """
        :param pre_process_func: A function that pre_processes the request parameters, before sending the request.
        :param post_process_func: A function that post_processes the result of the request, before returning it.
        :param request_func: The function that sends the request to the server.
        :param kwargs: The named parameters of the request. (Note: args where transformed to kwargs in the clientAPI.)

        If parameters are not named in post, get, or files, they are default sent as post parameters.
        """
        self._internal_job_id = str(uuid4())
        self.preprocess_func = pre_process_func
        self.post_process_func = post_process_func
        self._request_func = request_func
        self.job_statistics = JobStatistics()
        self.result = None
        self.error_msg = None

        # status to proceed
        self.status = JobStatus.CREATED
        self.time_out_at = datetime.utcnow() + timedelta(seconds=timeout)

        # prepare payload
        self.raw_payload = kwargs  # will be modified in job.preprocess_params in client.run
        self.payload = None  # will be prepared for post, get, and file params in client before request is sent

    def request(self):
        """
        Send the request initially to the server or get the status of a job from the server by job_id
        """
        self.job_statistics.request_send_at = datetime.utcnow()
        self.status = JobStatus.JOB_SEND
        try:
            self.result = self._request_func(self)
        except Exception as e:
            self.status = JobStatus.FAILED
            self.error_msg = str(e)
        return self

    def pre_process_params(self):
        """
        This function is called before the request is sent.
        Use it to modify the request payload parameters if needed.
        It is better to do it here than in the init function because this method will be called threaded.
        :param kwargs:
        :return:
        """
        if self.preprocess_func is not None:
            self.status = JobStatus.PRE_PROCESSING
            self.job_statistics.pre_processing_started_at = datetime.utcnow()
            self.raw_payload = self.preprocess_func(**self.raw_payload)
            self.job_statistics.pre_processing_ended_at = datetime.utcnow()

        return self.raw_payload

    def post_process_result(self, *args, **kwargs):
        """
        The result of the request is the raw response from the server.
        Use this method to process the result before returning it.
        :param result:
        :param kwargs:
        :return:
        """
        if self.post_process_func is not None and self.result is not None:
            self.status = JobStatus.POST_PROCESSING
            self.job_statistics.post_processing_started_at = datetime.utcnow()
            self.result = self.post_process_func(self.result, *args, **kwargs)
            self.job_statistics.post_processing_ended_at = datetime.utcnow()
            self.status = JobStatus.FINISHED

        return self

    def job_ended(self):
        """
        Check if the job has finished, failed, or timeout.
        """
        return self.status in [JobStatus.FINISHED, JobStatus.FAILED, JobStatus.TIMEOUT]
