"""Public analytics helpers of the socaity SDK."""
from typing import Any, Dict, List, Optional

from socaity_schemas.platform import EndpointPricing, EndpointStats, PriceEstimate, SimilarService

from socaity.core.catalog import _backend


def estimate(
    deployment_id: str,
    endpoint_id: Optional[str] = None,
    input_data: Optional[Dict[str, Any]] = None,
) -> Optional[PriceEstimate]:
    return _backend().estimate(deployment_id, endpoint_id=endpoint_id, input_data=input_data)


def get_stats(
    deployment_id: Optional[str] = None,
    endpoint_path: Optional[str] = None,
) -> List[EndpointStats]:
    return _backend().get_stats(deployment_id=deployment_id, endpoint_path=endpoint_path)


def get_similar_services(service_id: str, k: int = 8) -> List[SimilarService]:
    return _backend().get_similar_services(service_id, k=k)


def get_service_pricing(
    service_id: Optional[str] = None,
    deployment_id: Optional[str] = None,
    endpoint_id: Optional[str] = None,
) -> List[EndpointPricing]:
    return _backend().get_service_pricing(
        service_id=service_id,
        deployment_id=deployment_id,
        endpoint_id=endpoint_id,
    )
