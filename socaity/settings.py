import os

# The basis URL of all SOCAITY services.
# If not specified differently when a class is instantiated requests are sent to this URL.
DEFAULT_SOCAITY_URL = 'http://socaity.ai/api'
# For services hosted on runpod, an API key is required.
# If a service client calls an endpoint on runpod, the API key is added to the request in the header.
RUNPOD_API_KEY = os.environ.get("RUNPOD_API_KEY", None)
