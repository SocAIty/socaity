"""Compact JSON views of platform entities.

Catalog records carry far more than an agent needs to pick a service, and a raw
``model_dump`` of a hydrated ``AIService`` costs thousands of tokens per result.
These functions keep the fields an agent reasons about and drop the rest. Callers
that need everything can still fetch the record through the platform API.
"""

from __future__ import annotations

from typing import Any, List, Optional

from socaity_schemas.contract import Endpoint, EndpointParameter
from socaity_schemas.platform import AIModel, AIService, Job, Project

from socaity.tools.categories import names as category_names


def _unwrap(service: Any) -> AIService:
    """Return the underlying AIService of a lazy catalog wrapper."""
    return getattr(service, "raw", service)


def _description(entity: Any) -> Optional[str]:
    """Curated description wins; the agent copy is the fallback the platform keeps."""
    return getattr(entity, "description", None) or getattr(entity, "description_agent", None)


def service_summary(service: Any) -> dict:
    """One catalog hit: enough to compare candidates, not enough to run one."""
    service = _unwrap(service)
    return {
        "id": service.id,
        "name": service.name,
        "display_name": service.display_name,
        "description": service.short_desc or _description(service),
        "categories": category_names(service.categories),
        "models": [model.name for model in service.models],
        "is_official": service.is_official,
        "is_validated": service.is_validated,
        "is_public": service.is_public,
        "nsfw": service.nsfw,
        "n_usages": service.n_usages,
    }


def parameter_summary(parameter: EndpointParameter) -> dict:
    definition = parameter.definition
    if isinstance(definition, list):
        definition = definition[0] if definition else None
    return {
        "name": parameter.name,
        "type": getattr(definition, "type", None),
        "format": getattr(definition, "format", None),
        "enum": getattr(definition, "enum", None),
        "required": parameter.required,
        "default": parameter.default,
        "description": parameter.description,
    }


def endpoint_summary(endpoint: Endpoint) -> dict:
    return {
        "path": endpoint.path,
        "description": endpoint.description,
        "supports_streaming": endpoint.supports_streaming,
        "standard_schema": endpoint.standard_schema,
        "parameters": [parameter_summary(parameter) for parameter in endpoint.parameters],
    }


def service_detail(service: Any, endpoints: Optional[List[Endpoint]] = None) -> dict:
    """Full picture of one service, including the call signature of its endpoints."""
    service = _unwrap(service)
    detail = service_summary(service)
    detail.update(
        {
            "description": _description(service),
            "github_url": service.github_url,
            "has_billing": service.has_billing,
            "endpoints": [endpoint_summary(endpoint) for endpoint in endpoints or []],
        }
    )
    return detail


def model_summary(model: AIModel) -> dict:
    capabilities = model.capabilities
    return {
        "id": model.id,
        "name": model.name,
        "display_name": model.display_name,
        "description": _description(model),
        "family": model.family,
        "tasks": capabilities.tasks if capabilities else [],
        "input_modalities": capabilities.input_modalities if capabilities else [],
        "output_modalities": capabilities.output_modalities if capabilities else [],
        "context_window": capabilities.context_window if capabilities else None,
        "license": model.license.license_type if model.license else None,
        "hugging_face_url": model.hugging_face_url,
    }


def job_summary(job: Job) -> dict:
    return {
        "id": job.id,
        "status": job.status,
        "service_id": job.service_id,
        "endpoint": job.endpoint,
        "created_at": job.created_at,
        "finished_at": job.finished_at,
        "files": [file.url for file in job.files if file.url],
        "cost": job.billing.cost_amount if job.billing else None,
        "execution_time_s": job.billing.execution_time_s if job.billing else None,
        "display_name": job.data.display_name if job.data else None,
    }


def project_summary(project: Project) -> dict:
    return {
        "id": project.id,
        "display_name": project.display_name,
        "description": project.description,
        "created_at": project.created_at,
        "n_jobs": project.n_jobs,
        "n_files": project.n_files,
        "n_chats": project.n_chats,
    }


def page(items: List[dict], limit: int, offset: int) -> dict:
    """Wrap a result page with the cursor an agent needs to ask for the next one.

    ``next_offset`` is null on the last page, which is the signal to stop paging.
    """
    return {
        "items": items,
        "limit": limit,
        "offset": offset,
        "count": len(items),
        "next_offset": offset + len(items) if len(items) == limit else None,
    }
