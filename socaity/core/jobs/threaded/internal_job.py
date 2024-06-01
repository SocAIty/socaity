from datetime import datetime


class JobStatistics:
    """
    Stores the interval_sec when the different stages of the job were executed.
    """
    def __init__(self):
        self.created_at = datetime.utcnow()
        self.pre_processing_started_at = None   # job was added to queue and preprocessing has started
        self.pre_processing_ended_at = None
        self.request_send_at = None  # request was sent to server
        self.last_status_update_at = None  # for async_jobs jobs a new status was fetched
        self.request_result_received_at = None  # request result was received (server has finished job)
        self.post_processing_started_at = None  # post processing has started
        self.post_processing_ended_at = None
        self._execution_time = None

    def get_execution_time(self):
        """
        The interval_sec it took/takes to execute the job in seconds.
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


