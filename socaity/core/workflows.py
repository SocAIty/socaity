"""Public workflow helpers of the socaity SDK.

Thin layer over ``/v1/workflows`` (catalog, revisions, runs) and the workflow
estimate. Execution lives in ``socaity.tools.workflows`` (gateway job).
"""
from typing import Any, Dict, List, Optional, Union

from socaity_schemas.platform.workflow import (
    Workflow,
    WorkflowDocument,
    WorkflowEstimate,
    WorkflowLayout,
    WorkflowRevision,
    WorkflowRun,
    WorkflowUpsertResult,
)

from socaity.core.catalog import _backend


def list_workflows(
    q: Optional[str] = None,
    filters: Optional[List[str]] = None,
    expand: Optional[List[str]] = None,
    fields: Optional[List[str]] = None,
    sort: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
) -> List[Workflow]:
    """List or fuzzy-search workflows (your own plus public ones).

    Filters use the platform query grammar (``field:operator:value``), e.g.
    ``["slug:eq:my-flow"]`` or ``["visibility:eq:mine"]``.
    """
    return _backend().search_workflows(
        query=q, filters=filters, expand=expand, fields=fields, sort=sort, limit=limit, offset=offset,
    )


def get_workflow(
    workflow_id: str,
    expand: Optional[List[str]] = None,
    revision_id: Optional[str] = None,
    version: Optional[int] = None,
) -> Optional[Workflow]:
    """Fetch one workflow by ``wf_`` id or slug; the document is embedded by default."""
    return _backend().get_workflow(workflow_id, expand=expand, revision_id=revision_id, version=version)


def save_workflow(
    document: Union[Dict[str, Any], WorkflowDocument],
    layout: Optional[Union[Dict[str, Any], WorkflowLayout]] = None,
    slug: Optional[str] = None,
    message: Optional[str] = None,
    fork: bool = False,
) -> Optional[WorkflowUpsertResult]:
    """Save a workflow document (create, revise, or fork). One revision per save."""
    return _backend().upsert_workflow(document, layout=layout, slug=slug, message=message, fork=fork)


def delete_workflow(workflow_id: str) -> bool:
    """Hard-delete a workflow the caller owns (cascades to revisions and runs)."""
    return _backend().delete_workflow(workflow_id)


def publish_workflow(workflow_id: str, revision_id: Optional[str] = None) -> Optional[Workflow]:
    """Publish a workflow: pins an immutable published revision."""
    return _backend().publish_workflow(workflow_id, revision_id=revision_id)


def revert_workflow(
    workflow_id: str,
    revision_id: Optional[str] = None,
    version: Optional[int] = None,
) -> Optional[WorkflowUpsertResult]:
    """Roll back to an earlier revision by creating a new draft with its content."""
    return _backend().revert_workflow(workflow_id, revision_id=revision_id, version=version)


def list_workflow_revisions(
    workflow_id: str,
    expand: Optional[List[str]] = None,
    limit: int = 50,
    offset: int = 0,
) -> List[WorkflowRevision]:
    """Revision history of one workflow, newest first."""
    return _backend().list_workflow_revisions(workflow_id, expand=expand, limit=limit, offset=offset)


def list_workflow_runs(
    workflow_id: Optional[str] = None,
    filters: Optional[List[str]] = None,
    expand: Optional[List[str]] = None,
    limit: int = 50,
    offset: int = 0,
) -> List[WorkflowRun]:
    """List the caller's workflow runs, optionally scoped to one workflow."""
    return _backend().query_workflow_runs(
        workflow_id=workflow_id, filters=filters, expand=expand, limit=limit, offset=offset,
    )


def get_workflow_run(run_id: str, expand: Optional[List[str]] = None) -> Optional[WorkflowRun]:
    """Fetch one workflow run by ``wr_`` id. Expand ``traces`` for per-node detail."""
    return _backend().get_workflow_run(run_id, expand=expand)


def estimate_workflow(
    document: Optional[Union[Dict[str, Any], WorkflowDocument]] = None,
    workflow: Optional[str] = None,
    revision_id: Optional[str] = None,
    version: Optional[int] = None,
) -> Optional[WorkflowEstimate]:
    """Estimate price and runtime of a workflow (inline document or stored selector)."""
    return _backend().estimate_workflow(
        document=document, workflow=workflow, revision_id=revision_id, version=version,
    )
