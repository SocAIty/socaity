import time
from typing import Union, List
from socaity.socaity_client.jobs.threaded.internal_job import InternalJob
from socaity.socaity_client.jobs.threaded.job_status import JOB_STATUS
from socaity.socaity_client.utils import flatten_list


def gather_generator(jobs: Union[List[InternalJob], List[InternalJob], InternalJob, list]):
    if not isinstance(jobs, list):
        jobs = [jobs]

    # flatten array
    jobs: List[InternalJob] = list(flatten_list(jobs))
    # start jobs that not have been started
    for job in jobs:
        if job.status == JOB_STATUS.CREATED:
            job.run()

    finished_jobs = []
    while len(jobs) > len(finished_jobs):
        for job in jobs:
            if job.finished() and job not in finished_jobs:
                finished_jobs.append(job)
                yield job

        time.sleep(0.1)


def gather_results(jobs: Union[List[InternalJob], List[InternalJob], InternalJob, list]):
    return list(gather_generator(jobs))
