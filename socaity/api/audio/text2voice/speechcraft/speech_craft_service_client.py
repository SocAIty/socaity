from fastsdk import AudioFile, MediaFile
from fastsdk.definitions.ai_model import AIModelDescription
from fastsdk.definitions.enums import ModelDomainTag
from fastsdk.client.definitions.service_adress import RunpodServiceAddress
from fastsdk.client.api_client import APIClient
from socaity.settings import DEFAULT_SOCAITY_URL

srvc_speechcraft = APIClient(
    service_name="speechcraft",
    service_urls={
        "socaity": f"{DEFAULT_SOCAITY_URL}/speechcraft",
        "runpod": "https://api.runpod.ai/v2/esgd0bzgrxtwn1/run",
        "socaity_local": "http://localhost:8000/v0/speechcraft",
        "localhost": "localhost:8009/api",
        "localhost_runpod": RunpodServiceAddress("localhost:8009")
    },
    model_description=AIModelDescription(
        model_name="bark",
        model_domain_tags=[ModelDomainTag.IMAGE, ModelDomainTag.AUDIO]
    )
)
srvc_speechcraft.add_endpoint(
    endpoint_route="/text2voice",
    body_params={
        "text": str,
        "voice": str,
        "semantic_temp": float,
        "semantic_top_k": int,
        "semantic_top_p": float,
        "coarse_temp": float,
        "coarse_top_k": int,
        "coarse_top_p": float,
        "fine_temp": float
    },
    file_params={"voice": MediaFile},
    refresh_interval_s=2
)

srvc_speechcraft.add_endpoint(
    endpoint_route="voice2embedding",
    body_params={"voice_name": str, "save": bool},
    file_params={"audio_file": AudioFile},
    refresh_interval_s=2
)

srvc_speechcraft.add_endpoint(
    endpoint_route="voice2voice",
    body_params={
        "voice_name": str,
        "temp": float
    },
    file_params={"audio_file": AudioFile},
    refresh_interval_s=2
)
