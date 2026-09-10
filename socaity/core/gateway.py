"""Build a FastClient for a gateway factory path.

Agent turns and workflow runs are not catalog services. FastSDK still
requires an ``AIService`` plus ``Endpoint`` to run the job lifecycle, so
this module constructs that pair locally and returns a client that talks
through ``submit_job`` / ``track_job``.
"""
from __future__ import annotations

import hashlib

from apipod_registry import create_service
from fastsdk import FastSDK
from fastsdk.fastClient import FastClient
from socaity_schemas.contract import Endpoint, ServiceContract
from socaity_schemas.contract.address import SocaityServiceAddress

_GATEWAY_PREFIX = "_socaity_gateway"


def gateway_client(
    origin: str,
    api_key: str | None,
    path: str,
    materialize_media: bool,
) -> FastClient:
    """Return a temporary FastClient whose contract has exactly ``path``.

    The stand-in is registered in memory only. ``FastClient(service=...)``
    would persist it through the file-backed catalog store.
    """
    origin = origin.rstrip("/")
    normalized = path if path.startswith("/") else f"/{path}"
    digest = hashlib.sha256(f"{origin}{normalized}".encode()).hexdigest()[:16]
    service_id = f"{_GATEWAY_PREFIX}_{digest}"
    contract = ServiceContract(
        title="Socaity gateway",
        specification="apipod",
        has_job_queue=True,
        endpoints=[
            Endpoint(
                path=normalized,
                method="POST",
                request_body_content_type="application/json",
                supports_streaming=True,
            )
        ],
    )
    service = create_service(
        contract,
        address=SocaityServiceAddress(base_url=origin, path=""),
        provider="socaity",
        service_id=service_id,
        name=service_id,
    )
    FastSDK().service_registry.add_service(service, persist=False)
    return FastClient(
        service_name_or_id=service_id,
        api_key=api_key,
        temporary=True,
        materialize_media=materialize_media,
    )
