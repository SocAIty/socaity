from fastsdk.definitions.ai_model import AIModelDescription
from fastsdk.definitions.enums import ModelDomainTag
from fastsdk.web.service_client import ServiceClient
from pydantic import BaseModel, Field

from media_toolkit import ImageFile
from socaity.settings import DEFAULT_SOCAITY_URL

# Service Client for SAM 2
srvc_photomaker = ServiceClient(
    service_urls={
        "socaity": f"{DEFAULT_SOCAITY_URL}/tencentarc-photomaker",
        "replicate": {"version": "467d062309da518648ba89d226490e02b8ed09b5abc15026e54e31c5a8cd0769" },
    },
    service_name="tencentarc-photomaker",
    model_description=AIModelDescription(
        model_name="tencentarc-photomaker",
        model_domain_tags=[ModelDomainTag.IMAGE],
    ),
    upload_to_cloud_threshold_mb=0
)

# Input schema for the SAM 2 endpoint
class PhotoMakerInput(BaseModel):
    prompt: str = Field(default="", description="What kind of image do you want to create?")
    style_name: str = Field(default="", description="Use a specific style template")
    negative_prompt: str = Field(default="nsfw, lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry",
                                 description="Negative Prompt. The negative prompt should NOT contain the trigger word.")
    num_steps: int = Field(default=50, gt=0, lt=100)
    style_strength_ratio: float = Field(default=35, gt=0, le=50)
    num_outputs: int = Field(default=1, gt=0, le=4)
    guidance_scale: float = Field(default=5, ge=0, le=10)
    seed: int = Field(default=32, ge=0)
    disable_safety_checker: bool = Field(default=False, description="Disable safety checker")


# Add endpoint to the service client
srvc_photomaker.add_endpoint(
    endpoint_route="/generate",
    query_params=PhotoMakerInput(),
    file_params={
        "input_image": ImageFile,
        "input_image2": ImageFile,
        "input_image3": ImageFile,
        "input_image4": ImageFile,
    },
    refresh_interval_s=1,
)
