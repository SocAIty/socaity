import os
from fastsdk.settings import API_KEYS

# The basis URL of all SOCAITY services.
# If not specified differently when a class is instantiated requests are sent to this URL.
DEFAULT_SOCAITY_URL = os.environ.get("SOCAITY_API_URL", 'http://socaity.ai/api/v0')
DEFAULT_REPLICATE_URL = os.environ.get("REPLICATE_API_URL", "https://api.replicate.com/v1/models")


# For services hosted on runpod, an API key is required.
# If a service client calls an endpoint with one of those, the API key is added to the request in the header.
API_KEYS["socaity"] = os.getenv("SOCAITY_API_KEY", None)
API_KEYS["runpod"] = os.environ.get("RUNPOD_API_KEY", None)
API_KEYS["replicate"] = os.environ.get("REPLICATE_API_KEY", None)

