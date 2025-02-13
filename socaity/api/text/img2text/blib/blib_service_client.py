from fastsdk.definitions.ai_model import AIModelDescription
from fastsdk.definitions.enums import ModelDomainTag
from fastsdk.web.service_client import ServiceClient
from media_toolkit import ImageFile
from socaity.settings import DEFAULT_SOCAITY_URL, DEFAULT_REPLICATE_URL

srvc_blip = ServiceClient(
    service_urls={
        "socaity": f"{DEFAULT_SOCAITY_URL}/blip",
        "socaity_local": "http://localhost:8000/api/v0/blip",
        "replicate": { "version": "2e1dddc8621f72155f24cf2e0adbde548458d3cab9f00c0139eea840d0ac4746"},
    },
    service_name="blip",
    model_description=AIModelDescription(
        model_name="blip",
        model_domain_tags=[ModelDomainTag.IMAGE, ModelDomainTag.TEXT]
    )
)

# Endpoint definitions
from pydantic import BaseModel, Field


class BlipInput(BaseModel):
    task: str = Field(default="image_captioning", description="The task to perform.")
    question: str = Field(default="", description="The question for the visual question answering task")
    caption: str = Field(default="", description="Type caption for the input image for image text matching task.")


# Add endpoint to the service client
srvc_blip.add_endpoint(
    endpoint_route="/capture",
    query_params=BlipInput(),
    file_params={"image": ImageFile},
    refresh_interval_s=0.3
)
