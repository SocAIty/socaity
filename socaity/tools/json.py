"""JSON helpers for agent hosts (MCP pagination envelopes)."""

from __future__ import annotations

from typing import Any, List


def dump_entity(value: Any) -> Any:
    """JSON-ready view of a catalog entity or a backend dict."""
    if value is None:
        return None
    if hasattr(value, "raw"):
        value = value.raw
    if hasattr(value, "model_dump"):
        return value.model_dump(mode="json", exclude_none=True)
    if isinstance(value, list):
        return [dump_entity(item) for item in value]
    return value


def page(items: List[Any], limit: int, offset: int) -> dict:
    """Wrap a result page with the cursor an agent needs to ask for the next one."""
    rows = [dump_entity(item) for item in items]
    return {
        "items": rows,
        "limit": limit,
        "offset": offset,
        "count": len(rows),
        "next_offset": offset + len(rows) if len(rows) == limit else None,
    }
