"""Public HITL interrupt helpers of the socaity SDK."""

from typing import Any, Dict, List, Optional

from socaity_schemas.platform import Interrupt, InterruptResolveResult

from socaity.core.catalog import _backend


def query_interrupts(
    filters: Optional[List[str]] = None,
    expand: Optional[List[str]] = None,
    fields: Optional[List[str]] = None,
    sort: Optional[str] = None,
    limit: int = 100,
    offset: int = 0,
) -> List[Interrupt]:
    """Query your HIT action inbox. Pending rows by default; filter ``status`` for history.

    Filters use the platform query grammar (``field:operator:value``), e.g.
    ``["chat_id:eq:<uuid>"]`` or ``["status:eq:answered"]``.
    """
    return _backend().query_interrupts(
        filters=filters, expand=expand, fields=fields, sort=sort, limit=limit, offset=offset,
    )


def get_interrupt(
    interrupt_id: str,
    expand: Optional[List[str]] = None,
    fields: Optional[List[str]] = None,
) -> Optional[Interrupt]:
    """Fetch one action request by id. Expand ``chat``, ``chat_item`` or ``job`` as needed."""
    return _backend().get_interrupt(interrupt_id, expand=expand, fields=fields)


def resolve_interrupt(
    interrupt_id: str,
    decision: str,
    edited_action: Optional[Dict[str, Any]] = None,
    message: Optional[str] = None,
    continue_run: bool = True,
) -> Optional[InterruptResolveResult]:
    """Answer one HIT action: approve | edit | reject | respond.

    When the last action of the batch is answered and ``continue_run`` is true,
    the platform enqueues the agent continue job (returned on ``result.job``);
    stream or poll it like any other job.
    """
    return _backend().resolve_interrupt(
        interrupt_id,
        decision=decision,
        edited_action=edited_action,
        message=message,
        continue_run=continue_run,
    )
