from typing import TYPE_CHECKING

from media_toolkit import MediaFile, ImageFile, VideoFile, AudioFile
from fastsdk import (
    APISeex,
    FastClient,
    FastSDK,
    gather_results,
    gather_results_async,
    inspect_service,
    register_service,
)
from socaity_schemas.platform.catalog.model import AIModel
from socaity_schemas.platform.catalog.hosting import Deployment
from socaity_schemas.platform.jobs.job import Job
from socaity_schemas.platform.catalog.pricing import PriceEstimate
from socaity_schemas.platform.catalog.service import (
    Service,
    ServiceCategory,
    ServiceDetails,
)
from socaity.client import SocaityClient
from socaity.core.session import ActiveClient, Session, current_session

Client = SocaityClient

if TYPE_CHECKING:
    client: SocaityClient
else:
    client = ActiveClient()

service_registry = FastSDK().service_registry

__all__ = [
    "service_registry",
    "client",
    "Client",
    "SocaityClient",
    "Session",
    "current_session",
    "Job",
    "MediaFile",
    "ImageFile",
    "VideoFile",
    "AudioFile",
    "APISeex",
    "FastClient",
    "FastSDK",
    "gather_results",
    "gather_results_async",
    "inspect_service",
    "register_service",
    "Service",
    "ServiceDetails",
    "AIModel",
    "Deployment",
    "ServiceCategory",
    "PriceEstimate",
]
