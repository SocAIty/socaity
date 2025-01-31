from fastCloud import create_fast_cloud
from fastsdk.definitions.ai_model import AIModelDescription
from fastsdk.definitions.enums import ModelDomainTag
from fastsdk.web.service_client import ServiceClient
from socaity import DEFAULT_SOCAITY_URL


srvc_hunyuan_video = ServiceClient(
    service_urls={
        "socaity": f"{DEFAULT_SOCAITY_URL}/hunyuan_video",
        "socaity_local": "http://localhost:8000/api/v0/hunyuan_video",
        "replicate": {
            "version": "847dfa8b01e739637fc76f480ede0c1d76408e1d694b830b5dfb8e547bf98405"
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
    negative_prompt: str = Field(default="")
    width: int = Field(default=854)
    height: int = Field(default=480)
    video_length: int = Field(default=129)  # in frames
    infer_steps: int = Field(default=50)
    seed: int = Field(default=None)
    flow_shift: int = Field(default=7)
    embedded_guidance_scale: int = Field(default=False)


# ToDo: support pydantic schemas for default values..
srvc_hunyuan_video.add_endpoint(
    endpoint_route="/text2video",
    body_params=HunyuanVideoText2ImgPostParams(),
    refresh_interval_s=5
)