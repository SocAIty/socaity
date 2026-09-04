"""Public conversation helpers of the socaity SDK."""

from typing import List, Optional

from socaity_schemas.platform import Chat, ChatItem

from socaity.core.catalog import _backend


def query_conversations(
    q: Optional[str] = None,
    filters: Optional[List[str]] = None,
    expand: Optional[List[str]] = None,
    fields: Optional[List[str]] = None,
    sort: Optional[str] = None,
    limit: int = 100,
    offset: int = 0,
) -> List[Chat]:
    """Query your conversations, newest activity first.

    ``q`` is fuzzy full-text search (title, summary, message text). Filters use
    the platform query grammar, e.g. ``["status:eq:archived"]``.
    """
    return _backend().query_conversations(
        q=q, filters=filters, expand=expand, fields=fields, sort=sort, limit=limit, offset=offset,
    )


def get_conversation(
    conversation_id: str,
    expand: Optional[List[str]] = None,
    fields: Optional[List[str]] = None,
) -> Optional[Chat]:
    """Fetch one conversation by id. Expand ``items`` to embed every chat item."""
    return _backend().get_conversation(conversation_id, expand=expand, fields=fields)


def query_conversation_items(
    conversation_id: str,
    branch: str = "active",
    after: Optional[str] = None,
    order: str = "asc",
    filters: Optional[List[str]] = None,
    limit: int = 100,
) -> List[ChatItem]:
    """Items of one conversation.

    ``branch="active"`` walks the active parent chain; ``branch="all"`` returns
    the full tree. ``after`` is an item-id cursor for pagination.
    """
    return _backend().query_conversation_items(
        conversation_id, branch=branch, after=after, order=order, filters=filters, limit=limit,
    )


def update_conversation(
    conversation_id: str,
    title: Optional[str] = None,
    status: Optional[str] = None,
    active_item_id: Optional[str] = None,
) -> Optional[Chat]:
    """Rename, archive, or switch the active branch (``active_item_id``)."""
    return _backend().update_conversation(
        conversation_id, title=title, status=status, active_item_id=active_item_id,
    )


def fork_conversation(conversation_id: str) -> Optional[Chat]:
    """Copy the conversation tree into a new ``chats.id`` (new tab)."""
    return _backend().fork_conversation(conversation_id)


def delete_conversation(conversation_id: str) -> bool:
    """Soft-delete a conversation and clear its linked job data."""
    return _backend().delete_conversation(conversation_id)
