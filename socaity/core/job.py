import time


class Job:
    """
    A job is responsible for:
     - the logic for pre -and post-processing of a request to an endpoint
     - the payload to handle a request.
    Subclass it to implement run custom models.
    """
    def __init__(self, *args, **kwargs):
        self.created = time.time()

    def validate_params(self, *args, **kwargs):
        """
        The subclass can implement this method to validate the request parameters.
        :return:
        """
        pass

    def preprocess_params(self, *args, **kwargs):
        """
        This function is called before the request is send.
        Use it to modify the request parameters if needed.
        It is better to do it here than in the init function because this method will be called threaded.
        :param kwargs:
        :return:
        """
        return kwargs

    def postprocess_result(self, result, *args, **kwargs):
        """
        The result of the request is the raw response from the server.
        Use this method to process the result before returning it.
        :param result:
        :param kwargs:
        :return:
        """
        return result
