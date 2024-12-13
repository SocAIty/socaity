from fastCloud import create_cloud_storage
from fastsdk.definitions.ai_model import AIModelDescription
from fastsdk.definitions.enums import ModelDomainTag, ModelTag
from fastsdk.web.service_client import ServiceClient
from socaity import DEFAULT_SOCAITY_URL, AZURE_SAS_ACCESS_TOKEN, AZURE_SAS_CONNECTION_STRING, S3_ENDPOINT_URL, \
    S3_ACCESS_KEY_ID, S3_ACCESS_KEY_SECRET

srvc_flux_schnell = ServiceClient(
    service_urls={
        "socaity": f"{DEFAULT_SOCAITY_URL}/flux-schnell",
        "socaity_local": "http://localhost:8001/api/v0/flux-schnell",
        "replicate": "https://api.replicate.com/v1/models/black-forest-labs/flux-schnell/predictions",
    },
    service_name="flux-schnell",
    model_description=AIModelDescription(
        model_name="flux-schnell",
        model_domain_tags=[ModelDomainTag.IMAGE, ModelDomainTag.TEXT],
        model_tags=[ModelTag.TEXT2IMG]
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

from pydantic import BaseModel

class FluxText2ImgPostParams(BaseModel):
    prompt: str = ""
    aspect_ratio: str = "1:1"
    num_outputs: int = 1
    num_inference_steps: int = 4
    seed: int = None
    output_format: str = "jpg"
    disable_safety_checker: bool = False
    go_fast: bool = False


# ToDo: support pydantic schemas for default values..
srvc_flux_schnell.add_endpoint(
    endpoint_route="/text2img",
    post_params=FluxText2ImgPostParams(),
    #post_params={
    #    "prompt": str,
    #    "aspect_ratio": str,
    #    "num_outputs": int,
    #    "num_inference_steps": int,
    #    "seed": int,
    #    "output_format": str,
    #    "disable_safety_checker": bool,
    #    "go_fast": bool
    #},
    refresh_interval=2
)