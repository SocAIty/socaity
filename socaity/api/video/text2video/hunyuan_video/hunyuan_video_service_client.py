from fastsdk.definitions.ai_model import AIModelDescription
from fastsdk.definitions.enums import ModelDomainTag
from fastsdk.web.api_client import APIClient
from socaity.settings import DEFAULT_SOCAITY_URL


srvc_hunyuan_video = APIClient(
    service_urls={
        "socaity": f"{DEFAULT_SOCAITY_URL}/hunyuan-video",
        "socaity_local": "http://localhost:8000/v0/hunyuan-video",
        "replicate": {
            "version": "6c9132aee14409cd6568d030453f1ba50f5f3412b844fe67f78a9eb62d55664f"
        }
    },
    service_name="hunyuan-video",
    model_description=AIModelDescription(
        model_name="hunyuan-video",
        model_domain_tags=[ModelDomainTag.VIDEO, ModelDomainTag.TEXT]
    )
)

# Endpoint definitions

from pydantic import BaseModel, Field


class HunyuanVideoText2ImgPostParams(BaseModel):
    prompt: str = Field(default="")
    width: int = Field(default=864)
    height: int = Field(default=480)
    video_length: int = Field(default=129)  # in frames
    infer_steps: int = Field(default=50)
    seed: int = Field(default=None)
    embedded_guidance_scale: int = Field(default=False)


# ToDo: support pydantic schemas for default values..
srvc_hunyuan_video.add_endpoint(
    endpoint_route="/text2video",
    query_params=HunyuanVideoText2ImgPostParams(),
    refresh_interval_s=5
)