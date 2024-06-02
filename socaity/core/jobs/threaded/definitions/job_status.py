from enum import Enum


class JobStatus(Enum):
    """
    These status are used to keep track of the job status in the client (internally in the package)
    """
    CREATED = "created"  # job was internally created
    QUEUED = "queued"   # job was added to the internal job queue
    #PRE_PROCESSING = "preprocessing"  # job was taken from queue and preprocessing has started
    #JOB_SEND = "request_send"  # request (with payload) was sent to server
    #JOB_RESULT_RECEIVED = "job_result_received"  # server has finished job and result was received
    #POST_PROCESSING = "postprocessing"  # post processing has started
    FAILED = "failed"  # internal package error
    # TIMEOUT = "timeout"  # job waited too long for job_result_received
    REQUEST_TIMEOUT = "request_timeout"  # request took too long
    FINISHED = "finished"
