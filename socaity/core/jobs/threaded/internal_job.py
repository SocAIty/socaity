from datetime import datetime

from socaity.core.jobs.threaded.definitions.job_status import JobStatus


class InternalJob:

    def __init__(self, func: callable):
        self.func = func
        self.result = None
        self.error = None

        self.status = JobStatus.CREATED
        # timestamps
        self.created_at = datetime.utcnow()
        self.queued_at = None
        self.started_at = None
        self.finished_at = None

    def run(self):
        try:
            self.result = self.func()
        except Exception as e:
            self.error = e

    @property
    def is_done(self):
        return self.result is not None or self.error is not None