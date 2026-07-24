"""JSON-safe shapes for MCP tool responses (URLs, not in-memory media bytes)."""
from __future__ import annotations

from typing import Any

from pydantic import BaseModel


def to_jsonable(value: Any) -> Any:
    """Recursively convert SDK / media objects into JSON-serializable data."""
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, BaseModel):
        return to_jsonable(value.model_dump(mode="json", exclude_none=True))
    if isinstance(value, dict):
        return {str(k): to_jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [to_jsonable(v) for v in value]
    # media-toolkit files after materialize; prefer any known URL / name
    url = getattr(value, "url", None) or getattr(value, "path", None)
    file_name = getattr(value, "file_name", None)
    content_type = getattr(value, "content_type", None)
    if file_name is not None or content_type is not None or url is not None:
        return {
            "url": url if isinstance(url, str) and (url.startswith("http://") or url.startswith("https://")) else None,
            "file_name": file_name,
            "content_type": content_type,
            "note": "Binary content omitted. Use get_files with the url to download.",
        }
    if hasattr(value, "__dict__"):
        return to_jsonable(vars(value))
    return str(value)
