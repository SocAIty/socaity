from typing import Union

from socaity.core.client.client_factory import create_client
from socaity.core.job.async_server_job import AsyncServerJob
from socaity.core.job.job_queue import JobQueue
from socaity.globals import ModelType, EndPointType, EndpointSpecification
from socaity.core.job.job import Job


class ClientAPI:
    def __init__(self,
                 model_type: Union[ModelType, str] = ModelType.ANY,
                 model_name: str = "new_model",
                 endpoint_type: Union[EndPointType, str] = EndPointType.REMOTE,
                 endpoint_specification: EndpointSpecification = EndpointSpecification.SOCAITY,
                 *args, **kwargs
                 ):
        self.model_type = model_type
        self.model_name = model_name
        self.endpoint_type = endpoint_type
        # remote client, local client, decentralized ...
        self.client = create_client(
            model_type=model_type,
            model_name=model_name,
            endpoint_type=endpoint_type,
            endpoint_specification=endpoint_specification
        )
        self.job_queue = JobQueue()  # is a singleton

    def validate_params(self, *args, **kwargs) -> (bool, str):
        """
        Method is executed before a job is created.
        Validate the parameters passed to the job before job is created.
        :return: validation_success, error_message
        Subclass this method to implement your own validation.
        """
        return True, None

    def _pre_process(self, *args, **kwargs) -> dict:
        """
        This method is called before the job is executed.
        Subclass this method if you want to do some preprocessing of the args and kwargs.
        :return a dictionary with the parameters for the job.
        """
        return kwargs

    def _post_process(self, result, *args, **kwargs):
        """
        This method is called after the job is executed.
        Subclass this method if you want to do some postprocessing.
        """
        return result

    def create_job(self, **kwargs) -> Union[Job, AsyncServerJob, None]:
        """
        Create a job with the given parameters.
        This job is not yet added to the job queue. Call run_job() to add it to the job queue.
        Subclass this method if you want type hinting. But don't forget to call super().__call__(..)
        :kwargs: The parameters for running the job. Note only named are further passed to the job. Transform args to kwargs
        """
        return self.job_queue.create_job(
            request_func=self.client.request,
            pre_process_func=self._pre_process,
            post_process_func=self._post_process,
            refresh_job_status_func=self.client.refresh_job_status if hasattr(self.client,
                                                                              "refresh_job_status") else None,
            timeout=3600,
            **kwargs
        )

    def run_job(self, job: Union[Job, AsyncServerJob]) -> Union[Job, AsyncServerJob, None]:
        """
        Add a job to the job queue and run it.
        """
        self.job_queue.add_job(job)
        return job

    def __call__(self, **kwargs) -> Union[Job, AsyncServerJob, None]:
        """
        Run the job with the given parameters.
        Subclass this method if you want type hinting. But don't forget to call super().__call__(..)
        :kwargs: The parameters for running the job. Note only named are further passed to the job. Transform args to kwargs
        """
        valid, error = self.validate_params(**kwargs)
        if not valid:
            print(f"Validation of params failed before job execute: {error}. Job will not be created.")
            return None

        # The parameters for running the job are in *args and **kwargs and then stored in the job itself.
        job = self.create_job(**kwargs)
        job = self.run_job(job)
        return job

    def run(self, *args, **kwargs) -> Union[Job, AsyncServerJob, None]:
        """ Please subclass the class to implement type hinting."""
        return self(*args, **kwargs)

    def run_sync(self, *args, **kwargs) -> Union[Job, AsyncServerJob, None]:
        """
        Wait for the job to finish and return the result.
        """
        job = self.run(*args, **kwargs)
        if job is None:
            return None

        return self.job_queue.await_result(job)

