import functools
import inspect


class _JobManager:

    def __init__(self):
        self.job_queue = []

    @staticmethod
    def _job_progress_signature_change(func: callable) -> callable:
        # either param type is JobProgress or the name is job_progress
        for param in inspect.signature(func).parameters.values():
            if param.annotation == JobProgress or param.name == "job_progress":
                # exclude the job_progress parameter from the signature
                # note that because the queue_router_decorator_func was used before,
                # the job_progress param was already registered.
                new_sig = inspect.signature(func).replace(parameters=[
                    p for p in inspect.signature(func).parameters.values()
                    if p.name != "job_progress" or p.annotation != JobProgress
                ])
                func.__signature__ = new_sig
        return func

    def _create_job(self, job_function: callable, *args, **kwargs):
        job = Job(job_function)
        self.job_queue.append(job)
        return job


    def job(self):
        """
        Decorate your api function whith this decorator. @JobManager.job
        if your function is decorated it will return a job object instead of being executed synchronously.
        :return:
        """
        def decorator(func: callable):
            job_progress_modified = self._job_progress_signature_change(func)
            @functools.wraps(func)
            def wrapper(*wrapped_func_args, **wrapped_func_kwargs):
                return self._create_job(job_progress_modified, *wrapped_func_args, **wrapped_func_kwargs)

            return wrapper

        return decorator



JobManager = _JobManager()