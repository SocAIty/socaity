from fastsdk.definitions.ai_model import AIModelDescription
from fastsdk.definitions.enums import ModelDomainTag
from fastsdk.web.service_client import ServiceClient
from pydantic import BaseModel, Field

from media_toolkit import ImageFile
from socaity.settings import DEFAULT_SOCAITY_URL

# Service Client for SAM 2
srvc_sam2 = ServiceClient(
    service_urls={
        "socaity": f"{DEFAULT_SOCAITY_URL}/sam2",
        "replicate": {"version": "fe97b453a6455861e3bac769b441ca1f1086110da7466dbb65cf1eecfd60dc83" },
    },
    service_name="sam2",
    model_description=AIModelDescription(
        model_name="SAM 2",
        model_domain_tags=[ModelDomainTag.IMAGE, ModelDomainTag.MISC],
    ),
    upload_to_cloud_threshold_mb=0
)

# Input schema for the SAM 2 endpoint
class SAM2Input(BaseModel):
    points_per_side: int = Field(default=32, description="Number of points per side for segmentation.")
    pred_iou_thresh: float = Field(default=0.88, description="Prediction IoU threshold.")
    stability_score_thresh: float = Field(default=0.95, description="Stability score threshold.")
    use_m2m: bool = Field(default=True, description="Enable model-to-model interaction for segmentation.")


# Add endpoint to the service client
srvc_sam2.add_endpoint(
    endpoint_route="/segment",
    body_params=SAM2Input(),
    file_params={"image": ImageFile},
    refresh_interval_s=1,
)
