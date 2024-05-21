from socaity.core.job import Job
from socaity.core.job.job_queue import JobQueue


def await_results(jobs: [Job], default_return_on_error=None):
    """
    Wait for all jobs to finish and return results or default_return_on_error if any job failed.
    A job finishes if one of the events occur: result, error, timeout
    """
    for job in jobs:
        await_result(job, default_return_on_error)

    return jobs

def await_result(job: Job, default_return_on_error=None):
    """
    Wait for job to finish and return result or default_return_on_error if job failed.
    A job finishes if one of the events occur: result, error, timeout
    """
    return JobQueue().await_result(job, default_return_on_error)

def await_job(job: Job):
    """
    Wait for job to finish and return job.
    """
    return JobQueue().await_job(job)

