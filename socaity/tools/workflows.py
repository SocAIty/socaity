"""Workflow execution: submit a run to the inference gateway and wait for it.

``execute_workflow`` is the full-control core (progress and job-start hooks for
hosts that surface live progress, e.g. an MCP server or a terminal agent).
``run_workflow`` is the agent-facing tool with a schema-clean signature.

Unlike ``execute_service`` there is no per-service deployment address: workflow
runs go to the platform inference gateway (``POST /v1/workflows/{id}/run``) and
are polled on the standard ``GET /status/{job_id}`` route.
"""

from __future__ import annotations

from typing import Any, Callable, Optional

from socaity.tools.jobs import DEFAULT_POLL_INTERVAL_S, submit_and_poll


def execute_workflow(
    workflow: str,
    inputs: Optional[dict] = None,
    revision_id: Optional[str] = None,
    version: Optional[int] = None,
    workflow_run_id: Optional[str] = None,
    stream: bool = False,
    timeout_s: Optional[float] = None,
    poll_interval_s: float = DEFAULT_POLL_INTERVAL_S,
    on_progress: Optional[Callable[[float, str], None]] = None,
    on_job_start: Optional[Callable[[str, Any], None]] = None,
) -> dict:
    """Submit a workflow run and wait for its result (blocking core of ``run_workflow``).

    Args:
        workflow: Workflow ``wf_`` id or slug.
        inputs: Workflow-level input values, keyed as the document's inputs define.
        revision_id: ``rv_`` id to run; wins over ``version``.
        version: Valid version int; default is the latest valid revision.
        workflow_run_id: ``wr_`` id of an earlier run to continue / resume.
        stream: Stream run events over the job SSE channel (host-level feature).
        timeout_s: Give up waiting after this many seconds (the run keeps going).
        poll_interval_s: Delay between status polls of the running job.
        on_progress: Called with (progress 0..1, message) whenever progress changes.
        on_job_start: Called once with (platform job id, submit envelope) as soon
            as the gateway assigned an id. Hosts use it to surface live jobs.

    Returns:
        The terminal job envelope: ``job_id``, ``status``, ``result`` (the
        ``WorkflowRunResult`` with run id, outputs, pending actions), ``error``,
        ``metrics``. On timeout the status is "running" and the job keeps going.

    Raises:
        RuntimeError: When submission fails or the job reaches a terminal error state.
        ValueError: When no API key is available in the active session.
    """
    return submit_and_poll(
        f"/v1/workflows/{workflow}/run",
        {
            "inputs": inputs or {},
            "revision_id": revision_id,
            "version": version,
            "workflow_run_id": workflow_run_id,
            "stream": stream,
        },
        timeout_s=timeout_s,
        poll_interval_s=poll_interval_s,
        on_progress=on_progress,
        on_job_start=on_job_start,
        submit_error="Workflow run submit failed",
    )


def run_workflow(
    workflow: str,
    inputs: Optional[dict] = None,
    revision_id: Optional[str] = None,
    version: Optional[int] = None,
    workflow_run_id: Optional[str] = None,
    timeout_s: Optional[float] = None,
) -> dict:
    """Run a saved workflow and wait for its result.

    Call get_workflow first when you do not know the input names: the document's
    ``inputs`` section defines the keys ``inputs`` must carry. Use search_workflows
    to find the workflow by title, goal, or slug.

    The result carries the WorkflowRunResult: leaf node outputs keyed by node id,
    the ``workflow_run_id``, and (when the run paused for a human decision) the
    pending actions. Resume an interrupted run by answering its interrupts, or by
    calling this tool again with the same ``workflow_run_id``.

    Args:
        workflow: Workflow id (wf_...) or slug, as returned by search_workflows.
        inputs: Workflow input values, e.g. {"topic": "space travel"}. Keys must
            match the workflow document's declared inputs.
        revision_id: Revision to run (rv_...). Defaults to the latest valid one.
        version: Valid version number as an alternative to revision_id.
        workflow_run_id: Run id (wr_...) of an earlier run to continue or resume.
        timeout_s: Give up waiting after this many seconds. The run keeps going on
            the platform; poll it with get_workflow_run.

    Returns:
        job_id, status, and ``result`` containing the WorkflowRunResult (status,
        workflow_run_id, outputs, pending_actions). On timeout the status is
        "running" and the run is still visible via get_workflow_run.
    """
    return execute_workflow(
        workflow,
        inputs=inputs,
        revision_id=revision_id,
        version=version,
        workflow_run_id=workflow_run_id,
        timeout_s=timeout_s,
    )
