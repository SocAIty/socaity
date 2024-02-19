"""
This file contains a library of Jobs. A Job is added to a client to be run.
A Job is a class that contains the logic to pre and postprocess a request to an endpoint.
- The parameters of the __init__ method are the parameters of the request.
- The preprocess and postprocess methods are called before and after the request is made.
"""

from socaity.core.Job import Job


class text2speech(Job):
    def __init__(self, text, *args, **kwargs):
        super().__init__(text, *args, **kwargs)

    def validate_params(self, *args, **kwargs):
        pass
