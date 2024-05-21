from socaity.core.endpoint import EndPoint
from socaity.core.job.job import Job


class Client:
    """
    A Client handles the requests to an API.
    """

    def __init__(self, endpoint: EndPoint):
        self.endpoint = endpoint

    def __call__(self, *args, **kwargs):
        return self.request(*args, **kwargs)

    def request(self, job: Job):
        """
        The method to make the request to the API.
        Subclass this method.
        """
        raise NotImplementedError("Subclass the request method")



