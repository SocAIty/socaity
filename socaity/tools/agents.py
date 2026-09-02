"""Agent execution: talk to a deployed agent (e.g. SPAINE) as a platform job.

Base layer for remote agent usage: an agent is a catalog service
(``kind=agent``, ``execution=platform``), one turn is one job.
``execute_agent`` posts to the gateway factory ``POST /v1/agents/{id}/chat``
and polls the same ``GET /status/{job_id}`` as workflow and catalog jobs.
Higher layers (an ``Agent`` class, LangGraph adapters, the workflow engine
escalation) build on this without new transport.

Resume semantics: pass the same ``thread_id`` plus ``decisions`` to answer a
HIT interrupt, or the same ``thread_id`` with a new message to continue the
conversation. Thread state lives on the platform, not in this process.
"""

from __future__ import annotations

from typing import Any, Callable, Dict, List, Optional

from socaity.tools.jobs import DEFAULT_POLL_INTERVAL_S, submit_and_poll


def agent_payload(job: dict) -> dict:
    """Uniform agent-turn envelope from a ``job_payload`` dict."""
    response = job.get("result") if isinstance(job.get("result"), dict) else {}
    # Gateway stores the completion; some envelopes still wrap it as ``output``.
    if "choices" not in response and isinstance(response.get("output"), dict):
        response = response["output"]
    choices = response.get("choices") or []
    text = (choices[0].get("message") or {}).get("content") if choices else None
    return {
        "job_id": job.get("job_id"),
        "status": job.get("status"),
        "agent_status": response.get("status"),
        "thread_id": response.get("thread_id"),
        "text": text,
        "pending_actions": response.get("pending_actions") or [],
        "workflow": response.get("workflow"),
        "response": response,
    }


def execute_agent(
    agent: str,
    message: Optional[str] = None,
    messages: Optional[List[dict]] = None,
    thread_id: Optional[str] = None,
    mode: Optional[str] = None,
    model: Optional[str] = None,
    decisions: Optional[List[dict]] = None,
    continue_turn: bool = False,
    parent_item_id: Optional[str] = None,
    workflow: Optional[dict] = None,
    timeout_s: Optional[float] = None,
    poll_interval_s: float = DEFAULT_POLL_INTERVAL_S,
    on_progress: Optional[Callable[[float, str], None]] = None,
    on_job_start: Optional[Callable[[str, Any], None]] = None,
) -> dict:
    """Run one agent turn as a platform job and wait for it (blocking core).

    Args:
        agent: Agent service id, name or "owner/service" (catalog-resolved).
        message: Convenience single user message; appended to ``messages``.
        messages: Full ChatCompletion message list for the turn.
        thread_id: Conversation thread; reuse it to continue or resume.
        mode: Agent mode (SPAINE: chat | plan | agent | repair).
        model: Model override passed through to the agent.
        decisions: HIT decisions answering a previous ``pending_actions`` batch.
        continue_turn: After a cancel, invoke from the last checkpoint on the
            same thread and append to the cancelled assistant item (wire field
            ``continue``). Requires ``thread_id``; no message, no decisions.
        parent_item_id: Edit-and-fork: parent of the new user message (sibling
            branch). First-class request field. The orchestrator resolves the
            LangGraph checkpoint from that chat item. Empty string is root.
        workflow: Workflow document draft to seed the agent with.
        timeout_s: Give up waiting after this many seconds (job keeps running).
        poll_interval_s: Delay between progress samples of the running job.
        on_progress: Called with (progress 0..1, message) on progress changes.
        on_job_start: Called once with (platform job id, submit envelope).

    Returns:
        ``agent_payload`` dict: job_id, status, agent_status ("completed" or
        "interrupted"), thread_id, text (assistant reply), pending_actions,
        workflow (snapshot if the agent built one), response (raw payload).

    Raises:
        RuntimeError: When the job reaches a terminal error state.
        ValueError: When no message content was provided at all, or no API key.
    """
    turn_messages = list(messages or [])
    if message:
        turn_messages.append({"role": "user", "content": message})
    if continue_turn:
        if not thread_id:
            raise ValueError("continue_turn requires the thread_id of the cancelled turn.")
        if turn_messages or decisions:
            raise ValueError("continue_turn takes no messages and no decisions.")
    elif not turn_messages and not decisions:
        raise ValueError("execute_agent needs a message, messages, or decisions to resume with.")

    agent_config = {key: value for key, value in (("mode", mode), ("model", model)) if value}
    body: Dict[str, Any] = {"messages": turn_messages, "stream": False}
    if agent_config:
        body["agent"] = agent_config
    if continue_turn:
        body["continue"] = True
    if parent_item_id is not None:
        body["parent_item_id"] = parent_item_id
    for key, value in (("thread_id", thread_id), ("decisions", decisions), ("workflow", workflow)):
        if value:
            body[key] = value

    job = submit_and_poll(
        f"/v1/agents/{agent}/chat",
        body,
        timeout_s=timeout_s,
        poll_interval_s=poll_interval_s,
        on_progress=on_progress,
        on_job_start=on_job_start,
        submit_error="Agent turn submit failed",
    )
    return agent_payload(job)


def run_agent(
    agent: str,
    message: Optional[str] = None,
    thread_id: Optional[str] = None,
    mode: Optional[str] = None,
    decisions: Optional[List[dict]] = None,
    timeout_s: Optional[float] = None,
) -> dict:
    """Talk to a deployed agent and wait for its reply.

    One call is one agent turn. Start a conversation with just a message; the
    reply carries a ``thread_id``. Pass that same ``thread_id`` on the next call
    to continue, or together with ``decisions`` to answer the agent's
    ``pending_actions`` when it paused for approval (status "interrupted").

    Args:
        agent: Agent service id or name, e.g. "spaine", as found in the catalog.
        message: What you want the agent to do, as one user message.
        thread_id: Thread of an earlier turn to continue or resume.
        mode: Agent mode. SPAINE supports "chat" (answers), "plan" (designs a
            workflow), "agent" (acts with tools). Default is the agent's choice.
        decisions: Answers to a previous pending_actions batch, e.g.
            [{"interrupt_id": "...", "action": "approve"}].
        timeout_s: Give up waiting after this many seconds; the turn keeps
            running on the platform and its job stays pollable with get_job.

    Returns:
        status, agent_status ("completed" or "interrupted"), thread_id, text
        (the assistant reply), pending_actions (when interrupted), workflow
        (when the agent produced one), and job_id.
    """
    return execute_agent(
        agent,
        message=message,
        thread_id=thread_id,
        mode=mode,
        decisions=decisions,
        timeout_s=timeout_s,
    )
