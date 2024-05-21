import logging
from typing import Union,Tuple
import requests
from requests import JSONDecodeError

from socaity.core.client.client import Client
from socaity.core.endpoint import OpenAPIEndpoint
from socaity.core.job.job import Job


def web_request(
        url: str,
        get_params: dict = None,
        post_params: dict = None,
        files: dict = None) -> Tuple[object, Union[str, None]]:
    """
    Request an hosted API.
    :param url: The url of the API
    :param get_params: The parameters to be sent in the GET request
    :param post_params: The parameters to be sent in the POST request
    :param files: The files to be sent in the request.
    :return: result, error_msg (or None if nor error_msg occurred)
    """
    # add get parameters to url
    if get_params:
        url += "?"
        for k, v in get_params.items():
            url += f"{k}={v}&"
        url = url[:-1]

    # send request
    error = None
    res = None
    try:
        response = requests.post(url, params=post_params, files=files)
        if response.status_code == 404:
            error = f"API {url} not found."
            return None, error
        elif response.status_code == 500:
            logging.error(f"API {url} call error_msg: {response.content}")
            return None, response.content

        if response.headers.get("content-type") in ["audio/wav", "image/png", "image/jpg", "octet-stream"]:
            res = response.content
        else:
            res = response.json()
    except JSONDecodeError as e:
        logging.warning(f"Response of API {url} is not JSON format. Intended?")
        error = str(e)
    except Exception as e:
        error = str(e)
        logging.error(f"API {url} call error_msg: {str(e)}")

    return res, error


class OpenAPIClient(Client):
    """
    Used to interact with REST APIs that implement the openapi specification using web_requests.
    """
    def __init__(self, endpoint: OpenAPIEndpoint):
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

        # prepare the payload
        job = self.prepare_payload(job)

        res, error = web_request(url, job.payload["get_params"], job.payload["post_params"], job.payload["files"])

        if error:
            raise Exception(f"Error calling {url} error_msg: {error}")

        return res
