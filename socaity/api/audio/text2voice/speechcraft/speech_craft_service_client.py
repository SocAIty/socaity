from fastsdk import AudioFile
from fastsdk.definitions.enums import ModelDomainTag, ModelTag
from fastsdk.web.service_client import ServiceClient


srvc_speechcraft = ServiceClient(
    service_url="localhost:8009/api",
    model_name="bark",
    model_domain_tags=[ModelDomainTag.IMAGE, ModelDomainTag.AUDIO],
    model_tags=[ModelTag.FACE2FACE, ModelTag.IMAGE2IMAGE]
)
srvc_speechcraft.add_endpoint(
    endpoint_route="/text2voice",
    post_params={
        "text": str,
        "voice": str,
        "semantic_temp": float,
        "semantic_top_k": int,
        "semantic_top_p": float,
        "coarse_temp": float,
        "coarse_top_k": int,
        "coarse_top_p": float,
        "fine_temp": float
     }
)
srvc_speechcraft.add_endpoint(
    endpoint_route="voice2embedding",
    post_params={"voice_name": str, "save": bool},
    file_params={"audio_file": AudioFile}
)
srvc_speechcraft.add_endpoint(
    endpoint_route="voice2voice",
    post_params={"voice_name": str},
    file_params={"audio_file": AudioFile}
)

srvc_speechcraft.add_endpoint(endpoint_route="status", get_params={"job_id": str})

