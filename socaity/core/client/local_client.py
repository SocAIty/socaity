import logging
import threading
import time
import os
from subprocess import Popen, CREATE_NEW_CONSOLE
from enum import Enum

from socaity.core.job.job import Job
from socaity.core.client.openapi_client import OpenAPIClient, web_request
from socaity.core.endpoint import LocalEndPoint


class LocalServerStatus(Enum):
    INIT = "init"
    BOOTING = "booting"
    BUSY = "busy"
    RUNNING = "running"
    NOT_OK = "not ok"
    TIMEOUT = "timeout"


class LocalClient(OpenAPIClient):
    def __init__(self, endpoint: LocalEndPoint,
                 start_server_from_bat_file: bool = True,
                 server_not_reachable_timeout: int = 60
                 ):
        super().__init__(endpoint)
        self.endpoint = endpoint

        self.server_status = LocalServerStatus.INIT

        self.thread_lock = threading.Lock()  # prevents multiple attempts running to start the server
        self.__start_server_from_bat_file = start_server_from_bat_file
        self.server_not_reachable_timeout = server_not_reachable_timeout


    def _start_server(self) -> LocalServerStatus:
        if self.server_status != LocalServerStatus.INIT:
            return self.server_status

        # make a test request to check if the server is running
        if self.__check_server_status_ok() == LocalServerStatus.RUNNING:
            return LocalServerStatus.RUNNING

        if not os.path.isfile(self.endpoint.start_bat_path):
            raise ValueError(
                f"start_server.bat not found in {self.endpoint.start_bat_path}. "
                f"Is {self.endpoint.start_bat_path} installed?")

        # start the server in a new console
        self.server_status = LocalServerStatus.BOOTING
        logging.info(f"starting server {self.endpoint.start_bat_path}")
        self.process = Popen(
            self.endpoint.start_bat_path,
            creationflags=CREATE_NEW_CONSOLE,
            cwd=os.path.dirname(self.endpoint.start_bat_path)
        )

        status: LocalServerStatus = self._wait_for_ok_of_server()
        return status

    def _wait_for_ok_of_server(self) -> LocalServerStatus:
        # print("wait until bark is ready")
        start_open = time.time()

        ## not managed to print the console output in pipe don't know why it doesnt work.
        while True:
            status = self.__check_server_status_ok()
            if status == LocalServerStatus.RUNNING:
                logging.info("server is running")
                break
            elif int(time.time() - start_open) >= self.server_not_reachable_timeout:
                status = LocalServerStatus.TIMEOUT
                logging.error("timeout for starting server")
                break
            else:
                time.sleep(1)  # wait one sec

        return status

    def stop_server(self):
        if self.process is not None:
            self.process.terminate()
            self.server_status = LocalServerStatus.INIT

    def __check_server_status_ok(self) -> LocalServerStatus:
        """
        Check if the server is running and responding with "ok"
        """
        url = self.endpoint.service_url + "/status"
        status, error = web_request(url=url)
        if "ok" in str(status).lower() and not error:
            return LocalServerStatus.RUNNING
        elif "busy" in str(status).lower() and not error:
            return LocalServerStatus.BUSY
        elif error:
            return LocalServerStatus.NOT_OK
        else:
            return LocalServerStatus.BOOTING

    def request(self, job: Job):
        """
        Subclass of OpenAPIClient.request
        :param job: the job with the payload to send
        """
        # start the server if not running
        with self.thread_lock:
            if self.server_status.INIT:
                if self.__start_server_from_bat_file:
                    status: LocalServerStatus = self._start_server()
                    if status != LocalServerStatus.RUNNING:
                        raise ValueError(f"Failed to start server. Is {self.endpoint.start_bat_path} working?")
                else:
                    logging.info("Checking status of previously locally hosted server.")
                    status: LocalServerStatus = self._wait_for_ok_of_server()
                    if status != LocalServerStatus.RUNNING:
                        raise ValueError("Server is not running or returning status ok. Please start the server first.")

            elif self.server_status == LocalServerStatus.BUSY:
                logging.info("Server is busy. Waiting for it to be ready.")
                while self.server_status == LocalServerStatus.BUSY:
                    time.sleep(1)

            elif self.server_status == LocalServerStatus.NOT_OK:
                raise ValueError("A server error occured. Please restart the server.")

        # make the request
        result = super().request(job)
        return result
