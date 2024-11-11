import os
from fastsdk.settings import API_KEYS

# The basis URL of all SOCAITY services.
# If not specified differently when a class is instantiated requests are sent to this URL.
DEFAULT_SOCAITY_URL = 'http://socaity.ai/api/v0'
# For services hosted on runpod, an API key is required.
# If a service client calls an endpoint on runpod, the API key is added to the request in the header.
API_KEYS["socaity"] = os.getenv("SOCAITY_API_KEY", None)
API_KEYS["runpod"] = os.environ.get("RUNPOD_API_KEY", None)

# Cloud Storage
AZURE_SAS_ACCESS_TOKEN = os.environ.get("AZURE_SAS_ACCESS_TOKEN", None)
AZURE_SAS_CONNECTION_STRING = os.environ.get("AZURE_SAS_CONNECTION_STRING", None)
S3_ENDPOINT_URL = os.environ.get("S3_ENDPOINT_URL", None)
S3_ACCESS_KEY_ID = os.environ.get("S3_ACCESS_KEY_ID", None)
S3_ACCESS_KEY_SECRET = os.environ.get("S3_ACCESS_KEY_SECRET", None)
