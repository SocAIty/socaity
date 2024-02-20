from socaity.core.endpoint import EndPoint
from socaity.core.job import Job
import requests

class Client:
    """
    A Client handles the requests to an API.
    """

    def __init__(self, endpoint: EndPoint):
        self.endpoint = endpoint

        self._job_queue = []
        self._results = []

    def __call__(self, *args, **kwargs):
        return self.run(*args, **kwargs)

    def __prepare_payload(self, job: Job):
        """
        Subclass this method to implement your own payload preparation.
        This is for example needed in web requests to have post, get and file parameters.
        """
        return job.raw_payload

    def request(self, job: Job):
        """
        The method to make the request to the API.
        Subclass this method.
        """
        raise NotImplementedError("Subclass this method")

    def run(self, job: Job, *args, **kwargs):
        """
        Run the job.
        """
        # call pre_process function of client api (which is referenced in the job)
        job.pre_process_params()
        # obtain post, get, and files for web request
        job.payload = self.__prepare_payload(job)
        # make the request
        endpoint_result = self.request(job)  # result is also stored in the job
        # call post_process function of client api
        result = job.post_process_result(endpoint_result)
        return result

    def run_async(self):
        pass



