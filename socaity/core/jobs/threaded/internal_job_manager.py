from singleton_decorator import singleton

from socaity.core.jobs.threaded.internal_job import InternalJob


@singleton
class InternalJobManager:
    def __init__(self):
        self.queue = []

    def create_job_and_submit(self, func: callable):
        job = InternalJob(func=func)

    def submit(self, job: InternalJob):
        self.queue.append(job)

    def get_job(self, job_id: str):
        raise NotImplementedError("Implement in subclass")