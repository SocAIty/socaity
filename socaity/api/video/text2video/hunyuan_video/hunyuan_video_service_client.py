from fastCloud import create_cloud_storage
from fastsdk.definitions.ai_model import AIModelDescription
from fastsdk.definitions.enums import ModelDomainTag, ModelTag
from fastsdk.web.service_client import ServiceClient
from socaity import DEFAULT_SOCAITY_URL, AZURE_SAS_ACCESS_TOKEN, AZURE_SAS_CONNECTION_STRING, S3_ENDPOINT_URL, \
    S3_ACCESS_KEY_ID, S3_ACCESS_KEY_SECRET

srvc_hunyuan_video = ServiceClient(
    service_urls={
        "socaity": f"{DEFAULT_SOCAITY_URL}/hunyuan_video",
        "socaity_local": "http://localhost:8001/api/v0/hunyuan_video",
        "replicate": "https://api.replicate.com/v1/models/tencent/hunyuan-video/predictions"
    },
    service_name="hunyuan-video",
    model_description=AIModelDescription(
        model_name="hunyuan-video",
        model_domain_tags=[ModelDomainTag.VIDEO, ModelDomainTag.TEXT],
        model_tags=[ModelTag.TEXT2VIDEO]
    ),
    cloud_storage=create_cloud_storage(
        azure_sas_access_token=AZURE_SAS_ACCESS_TOKEN,
        azure_connection_string=AZURE_SAS_CONNECTION_STRING,
        s3_endpoint_url=S3_ENDPOINT_URL,
        s3_access_key_id=S3_ACCESS_KEY_ID,
        s3_access_key_secret=S3_ACCESS_KEY_SECRET
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
    post_params=HunyuanVideoText2ImgPostParams(),
    refresh_interval=5
)