import inspect
import time
import traceback
from datetime import datetime
from typing import Union
from uuid import uuid4

from socaity.socaity_client.jobs.threaded.internal_job_manager import InternalJobManager
from socaity.socaity_client.jobs.threaded.job_status import JOB_STATUS
from socaity.socaity_client.jobs.threaded.job_progress import JobProgress
from socaity.socaity_client.web.req.endpoint_request import EndPointRequest


class InternalJob:
    def __init__(
            self,
            job_function: callable,
            job_params: Union[dict, None],
            request_function: callable = None
    ):
        """
        Internal Job object to keep track of the job status and relevant information.
        :_job_function (callable): The function to execute
        :_job_params (dict): Parameters for the request
        :timeout (int): Timeout in seconds. If none timeout is set to one year.
        """
        self.id = str(uuid4())
        self._job_function = job_function
        self._job_params = job_params
        self.status: JOB_STATUS = JOB_STATUS.CREATED
        self.job_progress = JobProgress()

        # overwrite request function
        self._request_function = request_function
        self._ongoing_async_request: Union[EndPointRequest, None] = None

        self.result = None
        self.error = None

        # statistics
        self.created_at = datetime.utcnow()
        self.queued_at = None
        self.started_at = None
        self.finished_at = None

        # If true, the try catch block is not used, what makes debugging easier.
        self.debug_mode = False

    def request(self, endpoint_route: str, *args, **kwargs) -> EndPointRequest:
        self._ongoing_async_request = self._request_function(endpoint_route, True, *args, **kwargs)
        return self._ongoing_async_request

    def request_sync(self, endpoint_route: str, *args, **kwargs) -> EndPointRequest:
        self._ongoing_async_request = self._request_function(endpoint_route, False, *args, **kwargs)
        return self._ongoing_async_request

    def finished(self):
        """
        Returns true if job has ended. Either completed or by error.
        """
        return self.status in [JOB_STATUS.FINISHED, JOB_STATUS.FAILED]

    def has_started(self):
        return self.status in [JOB_STATUS.QUEUED, JOB_STATUS.PROCESSING]

    def wait_for_finished(self):
        if not self.has_started() and not self.finished():
            self.run()

        while not self.finished():
            time.sleep(0.1)
        return self

    def wait_for_request_result(self):
        if self._ongoing_async_request is None:
            return None

        return self._ongoing_async_request.wait_until_finished()

    @property
    def progress(self):
        # TODO: consider the web request
        return self.job_progress.get_progress()

    def set_progress(self, progress: float, message: str = None):
        self.job_progress.set_progress(progress, message)

    def _add_job_progress_to_kwargs(self):
        for param in inspect.signature(self._job_function).parameters.values():
            if param.annotation == InternalJob or param.name == "job":
                self._job_params[param.name] = self

        return self._job_params

    def _run(self):
        """
        function is called by internal job manager when job is executed
        """
        # run job
        self.started_at = datetime.utcnow()
        self.status = JOB_STATUS.PROCESSING
        try:
            self._add_job_progress_to_kwargs()  # add to job to jub_function if is in signature
            self.result = self._job_function(**self._job_params)
            self.set_progress(1.0, None)
            self.status = JOB_STATUS.FINISHED
        except Exception as e:
            self.status = JOB_STATUS.FAILED
            self.error = e
            self.finished_at = datetime.utcnow()
            if self.debug_mode:
                print(traceback.format_exc())

    def run_sync(self):
        return self.run(run_async=False)

    def run(self, run_async: bool = True):
        InternalJobManager.submit(self)
        if not run_async:
            self.wait_for_finished()
        return self


