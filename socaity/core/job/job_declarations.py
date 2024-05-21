from datetime import datetime
from enum import Enum


class JobStatistics:
    """
    Stores the time when the different stages of the job were executed.
    """
    def __init__(self):
        self.created_at = datetime.utcnow()
        self.pre_processing_started_at = None   # job was added to queue and preprocessing has started
        self.pre_processing_ended_at = None
        self.request_send_at = None  # request was sent to server
        self.last_status_update_at = None  # for async jobs a new status was fetched
        self.request_result_received_at = None  # request result was received (server has finished job)
        self.post_processing_started_at = None  # post processing has started
        self.post_processing_ended_at = None
        self._execution_time = None

    def get_execution_time(self):
        """
        The time it took/takes to execute the job in seconds.
        """
        # still running
        if self.post_processing_ended_at is None:
            return datetime.utcnow() - self.created_at

        # already finished
        if self._execution_time is not None:
            return self._execution_time

        # just finished
        self._execution_time = self.post_processing_ended_at - self.created_at
        return self._execution_time


class JobStatus(Enum):
    """
    These status are used to keep track of the job status in the client (internally in the package)
    """
    CREATED = "created"  # job was internally created
    QUEUED = "queued"   # job was added to the internal job queue
    PRE_PROCESSING = "preprocessing"  # job was taken from queue and preprocessing has started
    JOB_SEND = "request_send"  # request (with payload) was sent to server
    JOB_RESULT_RECEIVED = "job_result_received"  # server has finished job and result was received
    POST_PROCESSING = "postprocessing"  # post processing has started
    FAILED = "failed"  # internal package error
    TIMEOUT = "timeout"  # job waited too long for job_result_received
    REQUEST_TIMEOUT = "request_timeout"  # request took too long
    FINISHED = "finished"


class SocaityServerJobStatus(Enum):
    """
    These status are delivered by the server to indicate the current state of a submitted job to it
    If a job was send to a socaity server, with the job endpoint and the jobid, the server will return the status
    """
    QUEUED = "Queued"  # job was recieved by the server and is waiting there to be processed
    PROCESSING = "Processing"
    FINISHED = "Finished"
    FAILED = "Failed"
    TIMEOUT = "Timeout"
