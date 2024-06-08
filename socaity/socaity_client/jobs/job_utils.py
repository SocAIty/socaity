from typing import Union, List
from socaity.socaity_client.jobs.threaded.internal_job import InternalJob


def gather_results(jobs: Union[List[InternalJob], List[InternalJob], InternalJob, list]):

    if not isinstance(jobs, list):
        jobs = [jobs]

    results = []
    for job in jobs:
        # support nested jobs
        if isinstance(job, list):
            results.extend(gather_results(job))
            continue

        # wait for job result
        result = job.wait_for_finished()
        results.append(result)

    return results
