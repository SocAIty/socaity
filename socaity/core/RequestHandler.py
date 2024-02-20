import requests
from requests import JSONDecodeError


class RequestHandler:
    def __init__(self, api_url: str = "http://localhost:8000"):
        self.api_url = api_url

    def make_request(self, api_route):
        url = f"{self.api_url}/{api_route}"
        try:
            response = requests.get(url)
            res = response.json()
        except Exception as e:
            res = str(e)
            print(f"API {url} call error: {str(e)}")

        return res


    def post(self, api_route: str = "", payload: dict = None, files: dict = None):
        """
        :param api_route: which function to invoke
        :param payload: the parameters of the function to invoke
        :param files: parameters which are file are coming here
        :return:
        """

        url = f"{self.api_url}/{api_route}"
        res = None
        try:
            response = requests.post(url, params=payload, files=files, headers="")
            if response.status_code == 500:
                print(f"API {url} call error: {response.content}")
                return response.content

            if response.headers.get("content-type") in ["audio/wav", "image/png", "image/jpg", "octet-stream"]:
                res = response.content
            else:
                res = response.json()
        except JSONDecodeError as e:
            print(f"Response of API {url} is not JSON format. Intended?")
        except Exception as e:
            res = str(e)
            print(f"API {url} call error: {str(e)}")

        return res
