from typing import Union
import httpx

from socaity.core.web.definitions.socaity_server_response import SocaityServerResponse, SocaityServerJobStatus


def is_socaity_server_response(json: dict) -> bool:
    if not "endpoint_protocol" in json or json["endpoint_protocol"] != "socaity":
        return False

    required_fields = ["id", "status"]
    return all(field in json for field in required_fields)


def parse_response(response: httpx.Response) -> Union[SocaityServerResponse, bytes, dict, object]:
    """
    Parses the response of a request.
    :param response: The response of the request either formatted as json or the raw content
    :return: The parsed response as SocaityServerResponse or the raw content.
    """
    if response is None:
        return None

    if response.headers.get("Content-Type") == "application/json":
        result = response.json()
        #message = parse_status_code(response)

        if is_socaity_server_response(result):
            result['status'] = SocaityServerJobStatus(result['status'])
            result = SocaityServerResponse(**result)

        return result
    else:
        return response.content


def parse_status_code(response: httpx.Response):
    """
    Parses the status code of a response.
    :param response: The response of the request.
    :return: The status code of the response.
    """
    if response.status_code == 200:
        return None
    elif response.status_code == 404:
        return f"Endpoint {response.url} error: not found."
    elif response.status_code == 500:
        return f"Endpoint {response.url} error: {response.content}."

    return None

