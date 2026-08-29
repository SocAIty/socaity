from pathlib import Path

from media_toolkit import MediaFile, ImageFile, VideoFile, AudioFile
from fastsdk import (
    APISeex,
    FastClient,
    FastSDK,
    gather_results,
    gather_results_async,
    generate_stub,
    inspect_service,
    register_service,
)
from socaity_schemas.platform import (
    AIModel,
    AIService,
    Deployment,
    Job,
    PriceEstimate,
    ServiceCategory,
)
from socaity.core.socaity_service_registry import SocaityServiceRegistry
from socaity.core.session import Session, current_session, use_session
from socaity.core.catalog import (
    connect,
    get_model,
    get_service,
    list_categories,
    list_models,
    list_pricing_rules,
    list_services,
    search,
)
from socaity.core.jobs import (
    delete_job,
    get_job,
    list_jobs,
    refresh_job,
    update_job,
    update_social_metrics,
)
from socaity.core.files import (
    delete_file,
    get_file,
    get_storage_usage,
    list_files,
    update_file,
    upload_files,
)
from socaity.core.projects import (
    delete_project,
    get_project,
    list_projects,
    modify_project_members,
    upsert_project,
)
from socaity.core.conversations import (
    delete_conversation,
    get_conversation,
    list_conversation_items,
    list_conversations,
    update_conversation,
)
from socaity.core.interrupts import get_interrupt, list_interrupts, resolve_interrupt
from socaity.core.workflows import (
    delete_workflow,
    estimate_workflow,
    get_workflow,
    get_workflow_run,
    list_workflow_revisions,
    list_workflow_runs,
    list_workflows,
    publish_workflow,
    revert_workflow,
    save_workflow,
)
from socaity.core.analytics import (
    estimate,
    get_service_pricing,
    get_similar_services,
    get_stats,
)

service_registry = FastSDK().service_registry = SocaityServiceRegistry()

# Extend package search path so namespace imports resolve through sdk/:
#   socaity.official       -> socaity/sdk/official/
#   socaity.replicate.X    -> socaity/sdk/replicate/X/
#   socaity.{username}     -> socaity/sdk/community/{username}/
_sdk_root = Path(__file__).parent / "sdk"
__path__.append(str(_sdk_root))

_community_root = _sdk_root / "community"
if _community_root.exists():
    __path__.append(str(_community_root))


def install(service_name_or_id: str) -> None:
    """Install a specific service by name or ID."""
    if service_name_or_id == "all":
        service_registry.install_all()
    else:
        service_registry.install_service(service_name_or_id)


# Re-export official services at top level: from socaity import face2face
try:
    from socaity.sdk.official import *  # noqa: F401,F403
except ImportError:
    pass

__all__ = [
    "install",
    "service_registry",
    # session
    "Session",
    "current_session",
    "use_session",
    # catalog
    "list_services",
    "get_service",
    "list_models",
    "get_model",
    "list_categories",
    "list_pricing_rules",
    "search",
    "connect",
    # jobs
    "list_jobs",
    "get_job",
    "refresh_job",
    "update_job",
    "delete_job",
    "update_social_metrics",
    "Job",
    # files
    "list_files",
    "get_file",
    "get_storage_usage",
    "upload_files",
    "update_file",
    "delete_file",
    # projects
    "list_projects",
    "get_project",
    "upsert_project",
    "delete_project",
    "modify_project_members",
    # conversations
    "list_conversations",
    "get_conversation",
    "list_conversation_items",
    "update_conversation",
    "delete_conversation",
    # interrupts (HITL)
    "list_interrupts",
    "get_interrupt",
    "resolve_interrupt",
    # workflows
    "list_workflows",
    "get_workflow",
    "save_workflow",
    "delete_workflow",
    "publish_workflow",
    "revert_workflow",
    "list_workflow_revisions",
    "list_workflow_runs",
    "get_workflow_run",
    "estimate_workflow",
    # analytics
    "estimate",
    "get_stats",
    "get_similar_services",
    "get_service_pricing",
    # media
    "MediaFile",
    "ImageFile",
    "VideoFile",
    "AudioFile",
    # fastsdk
    "APISeex",
    "FastClient",
    "FastSDK",
    "gather_results",
    "gather_results_async",
    "generate_stub",
    "inspect_service",
    "register_service",
    # schemas
    "AIService",
    "AIModel",
    "Deployment",
    "ServiceCategory",
    "PriceEstimate",
]
