from fastsdk.definitions.enums import ModelDomainTag, ModelTag
from fastsdk.web.service_client import ServiceClient
from socaity import DEFAULT_SOCAITY_URL

srvc_flux_schnell = ServiceClient(
    service_urls={
        "socaity": f"{DEFAULT_SOCAITY_URL}/flux-schnell/api"
    },
    model_name="flux_schnell",
    model_domain_tags=[ModelDomainTag.TEXT, ModelDomainTag.IMAGE],
    model_tags=[ModelTag.TEXT2IMG]
)
srvc_flux_schnell.add_endpoint(
    endpoint_route="/text2img",
    post_params={
        "text": str,
        "aspect_ratio": str,
        "num_outputs": int,
        "num_inference_steps": int,
        "seed": int,
        "disable_safety_checker": float,
        "go_fast": bool
     },
    refresh_interval=2
)