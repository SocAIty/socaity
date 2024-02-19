from socaity.core.Endpoint import LocalEndPoint, EndPoint, RemoteEndPoint
import requests

class Client:
    """
    A Client handles the requests to an API.
    """

    def __init__(self, endpoint: EndPoint):
        self.endpoint = endpoint

    def __call__(self, *args, **kwargs):
        return self.run(*args, **kwargs)

    def pre_process(self, *args, **kwargs):
        pass

    def post_process(self, *args, **kwargs):
        pass

    def run(self, *args, **kwargs):
        # create_job(*kwargs).run()
        pass

    def run_async(self):
        pass




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

    def run(self):
        pass


class LocalClient(Client):
    def __init__(self, endpoint: LocalEndPoint):
        super().__init__(endpoint)


    def make_request(self, api_route):
        url = f"http://localhost:8000/{api_route}"
        try:
            response = requests.get(url)
            res = response.json()
        except Exception as e:
            res = str(e)
            print(f"API {url} call error: {str(e)}")

        return res



