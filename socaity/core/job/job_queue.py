import logging
from datetime import datetime
import time
import threading
from typing import Union

from singleton_decorator import singleton

from socaity.core.job.job import Job
from socaity.core.job.async_server_job import AsyncServerJob

from socaity.core.job.job_declarations import JobStatus


@singleton
class JobQueue:
    def __init__(self):
        self.queue = []
        self.in_progress = []  # a list of {"job_id": job._internal_job_id, "thread": t_job, "job": job}
        self.results = []
        self.worker_thread = threading.Thread(target=self.do_work, daemon=True)
        self.thread_lock = threading.Lock()
        self._previous_progress_lines = 0

    @staticmethod
    def create_job(
        request_func=None,
        pre_process_func=None,
        post_process_func=None,
        refresh_job_status_func=None,
        timeout=3600,
        **kwargs
    ) -> Union[Job, AsyncServerJob]:
        """
        Create a job with the given parameters.
        This job is not yet added to the job queue. Call add_job() to add it to the job queue.
        """
        job_class_ref = Job if refresh_job_status_func is None else AsyncServerJob
        return job_class_ref(
            refresh_func=refresh_job_status_func,
            pre_process_func=pre_process_func,
            post_process_func=post_process_func,
            request_func=request_func,
            timeout=timeout,
            **kwargs
        )

    def add_job(self, job: Union[Job, AsyncServerJob]) -> Union[Job, AsyncServerJob]:
        job.status = JobStatus.QUEUED
        self.queue.append(job)

        # start worker thread if not already done so
        if not self.worker_thread.is_alive():
            self.worker_thread.start()

        return job

    def process_job(self, job: Union[Job, AsyncServerJob]):
        # call pre_process function of client api (which is referenced in the job)
        job.pre_process_params()
        # make request with client. Method will wait for response until timeout is reached
        job.request()

        if type(job) is AsyncServerJob:
            # continuously ask for the job status until it is finished
            while not job.server_ended_job() and not job.job_ended():
                time.sleep(0.2)
                job.refresh_job_status()
        else:
            # if not async server job the request method is a nomral web_request that waits for the response
            job.job_statistics.request_result_received_at = datetime.utcnow()
            job.status = JobStatus.JOB_RESULT_RECEIVED

        # call client api.post_process function. Job just stores a reference to the function
        if not job.error_msg:
            job.post_process_result()

        self.results.append(job)

        logging.info(f"Job {job._internal_job_id} finished in {job.job_statistics.get_execution_time()}.")
        return job

    def do_work(self):
        while True:
            if len(self.queue) == 0 and len(self.in_progress) == 0:
                time.sleep(2)

            # create new jobs from queue
            for job in self.queue:
                t_job = threading.Thread(target=self.process_job, args=(job,), daemon=True)
                t_job.start()
                with self.thread_lock:
                    self.in_progress.append({"internal_job_id": job._internal_job_id, "thread": t_job, "job": job})
                    self.queue.remove(job)

            # check if jobs are finished
            for job_thread in self.in_progress:
                # remove finished jobs
                if not job_thread["thread"].is_alive():
                    with self.thread_lock:
                        self.in_progress.remove(job_thread)

                # remove timeout jobs
                # todo: use multiprocessing to be able to kill threads cleanly
                if job_thread["job"].time_out_at < datetime.utcnow():
                    # set status to failed
                    j = job_thread["job"]
                    j.status = JobStatus.TIMEOUT

                    with self.thread_lock:
                        self.in_progress.remove(job_thread)
                        self.results.append(j)
                        logging.info(f"Job {j._internal_job_id} finished in {job.job_statistics.get_execution_time()}.")

            self._show_progress_bar()

    def _show_progress_bar(self):
        # prints something like Job {_internal_job_id}; status: {Job.status}, %spinner%
        # in a actualizing overwriting manner
        # create a long string with all jobs and their status
        spinner = "◐◓◑◒"
        spinner_index = datetime.now().microsecond % len(spinner)
#
        p = ""
        if len(self.queue) > 0:
            p += f"Queue: {len(self.queue)} items {spinner[spinner_index]} "
        if len(self.in_progress) > 0:
            p += f"In progress: {len(self.in_progress)} items {spinner[spinner_index -1]} "

            # print progress of jobs if of type AsyncServerJob
            #for th in self.in_progress:
            #    job = th["job"]
            #    if type(job) is AsyncServerJob:
            #        if job.result is not None:
            #            p += f"id: {job.result.id}: status: {job.result.status}"
            #            if job.result.progress > 0:
            #                p += f"; progress: {job.result.progress}"
            #            p += "\n"

        if len(self.results) > 0:
            p += f"Finished: {len(self.results)} items"

        print(p, end="\r")

    def get_job(self, job_id: str) -> Union[Job, None]:
        """
        Get a job by its _internal_job_id. Returns None if the job does not exist.
        """
        # check if in results
        job = next((job for job in self.results if job._internal_job_id == job_id), None)
        if job:
            return job

        # check if in progress
        job = next((th['job'] for th in self.in_progress if th["_internal_job_id"] == job_id), None)
        if job:
            return job

        # return if in queue
        return next((job for job in self.queue if job._internal_job_id == job_id), None)

    def _wait_for_job_to_finish(self, job_or_jobid: Union[Job, AsyncServerJob, str]) -> Union[Job, None]:
        """
        Wait for the job to finish and return the result.
        :param job_or_jobid: The job object or the job _internal_job_id.
        """
        # check if in results
        job_id = job_or_jobid if type(job_or_jobid) is str else job_or_jobid._internal_job_id
        in_result = next((job for job in self.results if job._internal_job_id == job_id), False)

        while not in_result:
            time.sleep(1)
            in_result = next((job for job in self.results if job._internal_job_id == job_id), None)

        return in_result


    def await_job(self, job_or_jobid: Union[Job, AsyncServerJob, str]):
        """
        Wait for job to finish and return job. Delete job from results.
        """
        j = self._wait_for_job_to_finish(job_or_jobid)
        if j is not None:
            with self.thread_lock:
                self.results.remove(j)
        return j

    def await_result(self, job_or_jobid: Union[Job, AsyncServerJob, str], default_return_on_error=None):
        """
        Wait for job to finish and return result or default_return_on_error if job failed.
        """
        j = self.await_job(job_or_jobid)
        if j.result is not None:
            return j.result

        return default_return_on_error
