from socaity.core.Endpoint import LocalEndPoint, EndPoint, RemoteEndPoint
from socaity.core.Job import Job
import requests

class Client:
    """
    A Client handles the requests to an API.
    """

    def __init__(self, endpoint: EndPoint):
        self.endpoint = endpoint
        self.requestHandler = None

        self._job_queue = []
        self._results = []

    def __call__(self, *args, **kwargs):
        return self.run(*args, **kwargs)

    def make_request(self, job: Job, *args, **kwargs):
        """
        :param api_route: which function to invoke
        :param payload: the parameters of the function to invoke
        :param files: parameters which are file are coming here
        :return:
        """

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


    def run(self, job: Job, *args, **kwargs):
        job.preprocess_params()
        endpoint_result = self.make_request(job) # result is also stored in the job
        result = job.post_process_result(endpoint_result)
        return result

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

    def make_request(self, job: Job):
        try:
            response = requests.get(self.endpoint.url, headers=self.endpoint.headers)
            res = response.json()
        except Exception as e:
            res = str(e)
            print(f"API {self.endpoint.url} call error: {str(e)}")


    def run(self, job: Job, *args, **kwargs):
        super().run(job, *args, **kwargs)



class LocalClient(Client):
    def __init__(self, endpoint: LocalEndPoint):
        super().__init__(endpoint)
        self.is_running = False

    def _start_server(self):
        if not self.is_running:
            print("starting server")

            # make a test request to check if the server is running
            if self.__check_server_status_ok():
                return True

            if not os.path.isfile(self.start_bat_path):
                raise ValueError(
                    f"start_server.bat not found in {self.start_bat_path}. Is Bark installed?")
            # start the server in a new console
            print(f"starting server {self.start_bat_path}")
            self.process = Popen(self.start_bat_path,
                                 creationflags=CREATE_NEW_CONSOLE,
                                 cwd=os.path.dirname(self.start_bat_path)
                                 )

            # print("wait until bark is ready")
            start_open = time.time()

            ## not managed to print the console output in pipe don't know why it doesnt work.
            while True:
                status = self.__check_server_status_ok()
                if status:
                    print("server is running")
                    break
                elif int(time.time() - start_open) >= 60:
                    self.is_running = False
                    status = "timeout"
                    print("server start timed out")
                    break
                else:
                    time.sleep(1)  # wait one sec

            return status

    def stop_server(self):
        if not self.process is None:
            self.process.terminate()
            self.is_running = False

    def __check_server_status_ok(self):
        status = self.request_handler.make_request("status")
        if "ok" in str(status).lower():
            self.is_running = True
            return True
        else:
            return False





    def make_request(self, api_route):
        url = f"http://localhost:8000/{api_route}"
        try:
            response = requests.get(url)
            res = response.json()
        except Exception as e:
            res = str(e)
            print(f"API {url} call error: {str(e)}")

        return res



