"""Public conversation helpers of the socaity SDK."""

from typing import Optional

from socaity_schemas.platform import Chat

from socaity.core.catalog import _backend


def update_conversation(
    conversation_id: str,
    title: Optional[str] = None,
    status: Optional[str] = None,
) -> Optional[Chat]:
    """Rename or archive a conversation the caller owns."""
    return _backend().update_conversation(conversation_id, title=title, status=status)
