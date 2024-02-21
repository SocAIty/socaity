from typing import Union
import requests
from requests import JSONDecodeError

from socaity.core.client.client import Client
from socaity.core.endpoint import RemoteEndPoint
from socaity.core.job import Job


def web_request(url: str, get_params: dict = None, post_params: dict = None, files: dict = None):
    """
    The method to make the request to the API.
    """
    # add get parameters to url
    if get_params:
        url += "?"
        for k, v in get_params:
            url += f"{k}={v}&"
        url = url[:-1]

    # send request
    try:
        response = requests.post(url, params=post_params, files=files)
        if response.status_code == 500:
            print(f"API {url} call error: {response.content}")
            return response.content
        if response.headers.get("content-type") in ["audio/wav", "image/png", "image/jpg", "octet-stream"]:
            res = response.content
        else:
            res = response.json()
    except JSONDecodeError as e:
        print(f"Response of API {url} is not JSON format. Intended?")
        res = str(e)
    except Exception as e:
        res = str(e)
        print(f"API {url} call error: {str(e)}")

    return res

class RemoteClient(Client):
    """
    Used to interact with remote APIs. Implements Authentication and Authorization.
    It creates Jobs which are then run in a thread.
    The jobs have the required logic to pre and postprocess the requests.

    1. Get the token
    2. Make the request
    """
    def __init__(self, endpoint: RemoteEndPoint):
        super().__init__(endpoint)
        self.endpoint = endpoint

    def prepare_payload(self, job: Job) -> Job:
        """
        Moves params for post, get, and files.
        """
        # get the named parameters
        payload = {
            "post_params": {k: v for k, v in job.raw_payload.items() if k in self.endpoint.post_params},
            "get_params": {k: v for k, v in job.raw_payload.items() if k in self.endpoint.get_params},
            "files": {k: v for k, v in job.raw_payload.items() if k in self.endpoint.files}
        }

        # add remaining parameters to post
        remaining_params = {
            k: v for k, v in job.raw_payload.items()
            if k not in payload["post_params"]
            and k not in payload["files"]
            and k not in payload["get_params"]
        }
        payload["post_params"].update(remaining_params)

        job.payload = payload

        return job

    def request(self, job: Job) -> Union[dict, bytes, str, object, None]:
        """
        :param job: the job with the payload to send
        :return: the result of the request to the remote API
        """
        url = self.endpoint.service_url
        url = url if self.endpoint.endpoint_name is None else f"{url}/{self.endpoint.endpoint_name}"

        res = web_request(url, job.payload["get_params"], job.payload["post_params"], job.payload["files"])

        return res

    def run(self, job: Job, *args, **kwargs) -> Job:
        return super().run(job, *args, **kwargs)
