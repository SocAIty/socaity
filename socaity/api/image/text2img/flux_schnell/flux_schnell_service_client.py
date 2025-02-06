from fastsdk.definitions.ai_model import AIModelDescription
from fastsdk.definitions.enums import ModelDomainTag
from fastsdk.web.service_client import ServiceClient
from socaity.settings import DEFAULT_SOCAITY_URL, DEFAULT_REPLICATE_URL

srvc_flux_schnell = ServiceClient(
    service_urls={
        "socaity": f"{DEFAULT_SOCAITY_URL}/flux-schnell",
        "socaity_local": "http://localhost:8000/api/v0/flux-schnell",
        "replicate": f"{DEFAULT_REPLICATE_URL}/black-forest-labs/flux-schnell/predictions",
    },
    service_name="flux-schnell",
    model_description=AIModelDescription(
        model_name="flux-schnell",
        model_domain_tags=[ModelDomainTag.IMAGE, ModelDomainTag.TEXT]
    )
)

# Endpoint definitions

from pydantic import BaseModel, Field


class FluxText2ImgPostParams(BaseModel):
    prompt: str = Field(default="")
    aspect_ratio: str = Field(default="1:1")
    num_outputs: int = Field(default=1)
    num_inference_steps: int = Field(default=4, gt=0, lt=5)
    seed: int = Field(default=None)
    output_format: str = Field(default="jpg")
    disable_safety_checker: bool = Field(default=False)
    go_fast: bool = Field(default=False)


srvc_flux_schnell.add_endpoint(
    endpoint_route="/text2img",
    query_params=FluxText2ImgPostParams(),
    refresh_interval_s=2
)