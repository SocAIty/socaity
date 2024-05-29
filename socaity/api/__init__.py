"""
The references to ClientAPIs and SimpleAPIs

# CLIENT APIs
    A ServiceClientAPI is a class that contains the logic to pre and post_process a request to an endpoint.
    It is a wrapper around the client and job classes.
    Instead of using clients and jobs directly, you can use the predefined "model" ServiceClientAPI classes to do the work.

# SIMPLE APIs
    A SimpleAPI is a wrapper around a ServiceClientAPI.
    It initiates the ServiceClientAPI with the correct endpoint and model name, and provides a simple function to run the job.

"""
# Defined ClientAPIs
from .audio import *

# This references to all simple api functions
from .simple_api import *
from .await_result import await_result, await_results
