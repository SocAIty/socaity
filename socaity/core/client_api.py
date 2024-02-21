from typing import Union

from socaity.core.client.client_factory import create_client
from socaity.globals import ModelType, EndPointType
from socaity.core.job import Job


class ClientAPI:
    def __init__(self,
                 model_type: ModelType,
                 model_name: str,
                 endpoint_type: Union[EndPointType, str] = EndPointType.REMOTE
                 ):
        self.model_type = model_type
        self.model_name = model_name
        self.endpoint_type = endpoint_type
        self.client = create_client(model_type=model_type, model_name=model_name, endpoint_type=endpoint_type)

    def validate_params(self, *args, **kwargs) -> (bool, str):
        """
        Method is executed before a job is created.
        Validate the parameters passed to the job before job is created.
        :return: validation_success, error_message
        Subclass this method to implement your own validation.
        """
        return True, None

    def _pre_process(self, *args, **kwargs):
        """
        This method is called before the job is executed.
        Subclass this method if you want to do some preprocessing of the args and kwargs.
        """
        return args, kwargs

    def _post_process(self, *args, **kwargs):
        """
        This method is called after the job is executed.
        Subclass this method if you want to do some postprocessing.
        """
        pass

    def __call__(self, **kwargs) -> Union[Job, None]:
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
        job = Job(self._pre_process, self._post_process, **kwargs)

        result = self.client.run(job)
        #try:
        #    result = self.client.run(job)
        #except Exception as e:
        #    print(f"Job execution failed: {e}.")
        #    return None

        return result

    def run(self, *args, **kwargs):
        """ Please subclass the class to implement type hinting."""
        return self(*args, **kwargs)
