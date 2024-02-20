import requests
import time
import os
from subprocess import Popen, CREATE_NEW_CONSOLE
from enum import Enum

from socaity.core.Client.Client import Client
from socaity.core.Endpoint import LocalEndPoint

class LocalServerStatus(Enum):
    OK = "ok"
    NOT_OK = "not ok"
    TIMEOUT = "timeout"



class LocalClient(Client):
    def __init__(self, endpoint: LocalEndPoint,
                 start_server_from_bat_file: bool = True,
                 server_not_reachable_timeout: int = 60
                 ):
        super().__init__(endpoint)
        self.endpoint = endpoint
        self.is_running = False
        self.__start_server_from_bat_file = start_server_from_bat_file
        self.server_not_reachable_timeout = server_not_reachable_timeout

    def _start_server(self):
        if not self.is_running:
            print("starting server")

            # make a test request to check if the server is running
            if self.__check_server_status_ok():
                return True

            if not os.path.isfile(self.endpoint.start_bat_path):
                raise ValueError(
                    f"start_server.bat not found in {self.endpoint.start_bat_path}. Is Bark installed?")

            # start the server in a new console
            print(f"starting server {self.endpoint.start_bat_path}")
            self.process = Popen(self.endpoint.start_bat_path,
                                 creationflags=CREATE_NEW_CONSOLE,
                                 cwd=os.path.dirname(self.endpoint.start_bat_path)
                                 )

            status = self._wait_for_ok_of_server()

            return status

        
    def _wait_for_ok_of_server(self):
        # print("wait until bark is ready")
        start_open = time.time()

        ## not managed to print the console output in pipe don't know why it doesnt work.
        while True:
            status = self.__check_server_status_ok()
            if status:
                print("server is running")
                break
            elif int(time.time() - start_open) >= self.server_not_reachable_timeout:
                self.is_running = False
                status = LocalServerStatus.TIMEOUT
                print("server start timed out")
                break
            else:
                time.sleep(1)  # wait one sec

        return status

    def stop_server(self):
        if not self.process is None:
            self.process.terminate()
            self.is_running = False

    def __check_server_status_ok(self) -> LocalServerStatus:
        """
        Check if the server is running and responding with "ok"
        """
        status = self.request_handler.make_request("status")
        if "ok" in str(status).lower():
            self.is_running = True
            return LocalServerStatus.OK
        else:
            return LocalServerStatus.NOT_OK


    def make_request(self, api_route):

        if not self.is_running:
            if self.__start_server_from_bat_file:
                self._start_server()
            else:
                raise ValueError("Server is not running. Please start the server first.")

        url = f"http://localhost:8000/{api_route}"
        try:
            response = requests.get(url)
            res = response.json()
        except Exception as e:
            res = str(e)
            print(f"API {url} call error: {str(e)}")

        return res
