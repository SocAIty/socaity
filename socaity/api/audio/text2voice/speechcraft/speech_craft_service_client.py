from fastsdk import AudioFile, MediaFile
from fastsdk.definitions.ai_model import AIModelDescription
from fastsdk.definitions.enums import ModelDomainTag
from fastsdk.web.definitions.service_adress import RunpodServiceAddress
from fastsdk.web.service_client import ServiceClient


srvc_speechcraft = ServiceClient(
    service_name="speechcraft",
    service_urls={
        "localhost": "localhost:8009/api",
        "localhost_runpod": RunpodServiceAddress("localhost:8009"),
        "runpod": "https://api.runpod.ai/v2/esgd0bzgrxtwn1/run",
        "socaity_local": "http://localhost:8000/api/v0/speechcraft"
    },
    model_description=AIModelDescription(
        model_name="bark",
        model_domain_tags=[ModelDomainTag.IMAGE, ModelDomainTag.AUDIO]
    )
)
srvc_speechcraft.add_endpoint(
    endpoint_route="/text2voice",
    query_params={
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
    refresh_interval_s=2
)
srvc_speechcraft.add_endpoint(
    endpoint_route="/text2voice_with_embedding",
    query_params={
        "text": str,
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
    query_params={"voice_name": str, "save": bool},
    file_params={"audio_file": AudioFile},
    refresh_interval_s=2
)
srvc_speechcraft.add_endpoint(
    endpoint_route="voice2voice",
    query_params={
        "voice_name": str,
        "temp": float
    },
    file_params={"audio_file": AudioFile},
    refresh_interval_s=2
)
