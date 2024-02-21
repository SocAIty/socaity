import time


class JobStatistics:
    """
    Stores the time when the different stages of the job were executed.
    """
    def __init__(self):
        self.created = time.time()
        self.pre_processing_started = None
        self.pre_processing_ended = None
        self.request_send = None
        self.request_result_received = None
        self.post_processing_started = None
        self.post_processing_ended = None

    def get_execution_time(self):
        """
        The time it took to execute the job in seconds.
        """
        return self.post_processing_ended - self.pre_processing_started


class Job:
    """
    A job contains the:
     - the payload to handle a request.
     - references to the pre and post processing functions.
     - the result of the request.
     - the statistics and execution times of the job.
    """
    def __init__(self,
                 pre_process_func: callable = None,
                 post_process_func: callable = None,
                 **kwargs):
        """
        :param pre_process_func: A function that pre_processes the request parameters, before sending the request.
        :param post_process_func: A function that post_processes the result of the request, before returning it.
        :param kwargs: The named parameters of the request. (Note: args where transformed to kwargs in the clientAPI.)

        If parameters are not named in post, get, or files, they are default sent as post parameters.
        """

        self.preprocess_func = pre_process_func
        self.post_process_func = post_process_func
        self.job_statistics = JobStatistics()
        self.result = None

        # prepare payload
        self.raw_payload = kwargs  # will be modified in job.preprocess_params in client.run
        self.payload = None  # will be prepared for post, get, and file params in client before request is sent

    def get_payload(self):
        return self.payload

    def pre_process_params(self):
        """
        This function is called before the request is sent.
        Use it to modify the request payload parameters if needed.
        It is better to do it here than in the init function because this method will be called threaded.
        :param kwargs:
        :return:
        """
        if self.preprocess_func is not None:
            self.job_statistics.pre_processing_started = time.time()
            self.raw_payload = self.preprocess_func(**self.raw_payload)
            self.job_statistics.pre_processing_ended = time.time()

        return self.raw_payload

    def post_process_result(self, result, *args, **kwargs):
        """
        The result of the request is the raw response from the server.
        Use this method to process the result before returning it.
        :param result:
        :param kwargs:
        :return:
        """
        if self.post_process_func is not None:
            self.job_statistics.post_processing_started = time.time()
            self.result = self.post_process_func(result, *args, **kwargs)
            self.job_statistics.post_processing_ended = time.time()

        return self

