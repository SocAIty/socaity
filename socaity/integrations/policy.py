"""Function-identity policy for SDK tool exposure, run handling, and HIT."""
from __future__ import annotations

import inspect
from typing import Any, Callable, Iterable, List, Type, Union, get_args, get_origin

from pydantic import create_model

from socaity.client import SocaityClient
from socaity_cli.clients.conversations import ConversationsClient
from socaity_cli.clients.deployment import DeploymentClient
from socaity_cli.clients.files import FilesClient
from socaity_cli.clients.jobs import JobsClient
from socaity_cli.clients.profile import ProfileClient
from socaity_cli.clients.projects import ProjectsClient
from socaity_cli.clients.sdk_install import SdkInstallClient
from socaity_cli.clients.workflows import WorkflowsClient

PROGRAMMATIC_ONLY = frozenset({
    DeploymentClient.analyze_deployment,
    DeploymentClient.create_deployment_draft,
    DeploymentClient.upsert_hf_token,
    DeploymentClient.list_hf_tokens,
    DeploymentClient.get_registry_usage,
    DeploymentClient.get_push_credentials,
    DeploymentClient.confirm_image_pushed,
    DeploymentClient.get_deployment_pipeline_status,
    DeploymentClient.cancel_deployment_pipeline,
    DeploymentClient.upsert_ai_service,
    DeploymentClient.upsert_service_endpoint,
    DeploymentClient.upsert_deployment,
    DeploymentClient.upsert_service,
    DeploymentClient.order_async_deployment,
    DeploymentClient.get_deployment_status,
    DeploymentClient.is_dockerhub_repo_accessible,
    DeploymentClient.is_service_name_available,
    SdkInstallClient.install_service,
    SdkInstallClient.get_service_updates,
    ProfileClient.whoami,
    ProfileClient.exchange_cli_auth,
    FilesClient.upload_files,
    SocaityClient.connect,
    SocaityClient.track_job,
})

RUN_METHODS = frozenset({
    SocaityClient.run_service,
    SocaityClient.run_agent,
    SocaityClient.run_workflow,
})

DESTRUCTIVE_METHODS = frozenset({
    JobsClient.delete_job,
    FilesClient.delete_file,
    ProjectsClient.delete_project,
    ConversationsClient.delete_conversation,
    WorkflowsClient.delete_workflow,
    DeploymentClient.delete_service,
})


def iter_public_methods(client_type: Type = SocaityClient) -> Iterable[Callable]:
    """Yield unbound public methods of ``client_type``."""
    for name, method in inspect.getmembers(client_type, inspect.isfunction):
        if name.startswith("_"):
            continue
        yield method


def resolved_hints(method: Callable) -> dict:
    """Evaluate postponed annotations against the method's own module."""
    try:
        return inspect.get_type_hints(method, include_extras=True)
    except Exception:
        return dict(getattr(method, "__annotations__", {}) or {})


def json_return_annotation(hint):
    """JSON-facing return type: list or dict, after serialize_value."""
    origin = get_origin(hint)
    if origin is Union:
        args = get_args(hint)
        if type(None) in args:
            return Any
        non_none = [arg for arg in args if arg is not type(None)]
        if len(non_none) == 1:
            return json_return_annotation(non_none[0])
        return dict
    if origin in (list, tuple, set) or hint is list:
        return list
    return dict


def exposed_signature(method: Callable):
    """Signature of ``method`` with ``self`` removed and annotations resolved."""
    signature = inspect.signature(method)
    hints = resolved_hints(method)
    parameters = []
    for parameter in signature.parameters.values():
        if parameter.name == "self":
            continue
        annotation = hints.get(parameter.name, parameter.annotation)
        parameters.append(parameter.replace(annotation=annotation))
    return signature.replace(
        parameters=parameters,
        return_annotation=json_return_annotation(hints.get("return", dict)),
    )


def validate_tool_schema(method: Callable) -> None:
    """Fail if ``method`` cannot produce a Pydantic model for a JSON tool schema."""
    fields = {}
    try:
        hints = inspect.get_type_hints(method, include_extras=True)
    except Exception:
        hints = getattr(method, "__annotations__", {}) or {}
    for name, parameter in exposed_signature(method).parameters.items():
        if parameter.kind in (parameter.VAR_POSITIONAL, parameter.VAR_KEYWORD):
            continue
        annotation = hints.get(name, parameter.annotation)
        if annotation is inspect.Parameter.empty:
            annotation = object
        default = ... if parameter.default is inspect.Parameter.empty else parameter.default
        fields[name] = (annotation, default)
    try:
        create_model(f"{method.__name__}Args", **fields)
    except Exception as exc:
        raise RuntimeError(f"Method '{method.__name__}' cannot produce a JSON tool schema: {exc}") from exc


def iter_tool_methods(client_type: Type = SocaityClient) -> List[Callable]:
    """Public methods eligible as LLM tools, in definition order."""
    methods: List[Callable] = []
    names = set()
    public = list(iter_public_methods(client_type))
    _validate_policy(public)
    for method in public:
        if method in PROGRAMMATIC_ONLY:
            continue
        if method.__name__ in names:
            raise RuntimeError(f"Duplicate tool name: {method.__name__}")
        validate_tool_schema(method)
        names.add(method.__name__)
        methods.append(method)
    return methods


def tool_methods_by_name(client_type: Type = SocaityClient) -> dict:
    """Temporary name index for harness mode selection. Not a source of truth."""
    return {method.__name__: method for method in iter_tool_methods(client_type)}


def methods_named(*names: str, client_type: Type = SocaityClient) -> List[Callable]:
    """Look up canonical methods by name from the derived index."""
    index = tool_methods_by_name(client_type)
    missing = [name for name in names if name not in index]
    if missing:
        raise RuntimeError(f"Unknown tool methods: {missing}")
    return [index[name] for name in names]


def _validate_policy(public: List[Callable]) -> None:
    by_name = {method.__name__: method for method in public}
    for method in PROGRAMMATIC_ONLY | RUN_METHODS | DESTRUCTIVE_METHODS:
        found = by_name.get(method.__name__)
        if found is not method:
            raise RuntimeError(
                f"Policy references {method.__qualname__}, which is not a public method "
                f"of SocaityClient (found {getattr(found, '__qualname__', None)})."
            )
