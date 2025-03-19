from enum import Enum

from fastsdk.definitions.ai_model import AIModelDescription
from fastsdk.definitions.enums import ModelDomainTag
from fastsdk.web.api_client import APIClient
from media_toolkit import AudioFile
from socaity.settings import DEFAULT_SOCAITY_URL, DEFAULT_REPLICATE_URL

srvc_whisper = APIClient(
    service_urls={
        "socaity": f"{DEFAULT_SOCAITY_URL}/insanely-fast-whisper",
        "socaity_local": "http://localhost:8000/v0/insanely-fast-whisper",
        "replicate": { "version": "3ab86df6c8f54c11309d4d1f930ac292bad43ace52d10c80d87eb258b3c9f79c"},
    },
    service_name="insanely-fast-whisper",
    model_description=AIModelDescription(
        model_name="insanely-fast-whisper",
        model_domain_tags=[ModelDomainTag.IMAGE, ModelDomainTag.TEXT]
    ),
    upload_to_cloud_threshold_mb=0
)

class WhisperTasks(Enum):
    TRANSCRIBE = "transcribe"
    TRANSLATE = "translate"

class WhisperTimeStamp(Enum):
    CHUNK = "chunk"
    WORD = "word"


# Add endpoint to the service client
srvc_whisper.add_endpoint(
    endpoint_route="/transcribe",
    query_params= {
        "task": str,
        "language": str,
        "batch_size": int,
        "timestamp": str
    },
    file_params={"audio": AudioFile},
    refresh_interval_s=0.5
)
