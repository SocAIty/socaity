"""Credential-scoped access to the socaity backend.

The public helpers (``socaity.list_services``, ``socaity.connect``, ...) run against
the *current* session. In a single-user process that is the default session, which
picks up the API key from the environment or the stored CLI login, so nothing changes
for scripts and notebooks.

Hosts that serve several callers from one process (the MCP server) open one session
per request with ``use_session``. The session lives in a ``ContextVar``, so concurrent
tasks cannot observe or reuse each other's credentials.
"""
from __future__ import annotations

from contextlib import contextmanager
from contextvars import ContextVar
from pathlib import Path
from typing import Iterator, Optional

from socaity_cli import SocaityBackendClient


class Session:
    """One caller's credentials plus the backend client bound to them.

    Args:
        api_key: Socaity API key. ``None`` falls back to ``SOCAITY_API_KEY`` or the
            credentials written by ``socaity login``.
        backend_url: Override the backend base URL (tests, self-hosted deployments).
        materialize_media: Default for clients created through ``connect``. ``False``
            keeps file results as URL references instead of downloading the bytes.
        user_id: Caller id when the host already knows it (SPAINE, MCP).
        user_name: Display name for prompts. Never send ``api_key`` to a model.
        conversation_id: Current chat id, if the host has one.
        local_root: User-local sandbox root on the host. Local tools must stay inside it.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        backend_url: Optional[str] = None,
        materialize_media: bool = True,
        user_id: Optional[str] = None,
        user_name: str = "user",
        conversation_id: Optional[str] = None,
        local_root: Optional[Path] = None,
    ):
        self.api_key = api_key
        self.materialize_media = materialize_media
        self.backend = SocaityBackendClient(backend_url=backend_url, api_key=api_key)
        self.user_id = user_id
        self.user_name = user_name
        self.conversation_id = conversation_id
        self.local_root = local_root


_current: ContextVar[Optional[Session]] = ContextVar("socaity_session", default=None)
_default: Optional[Session] = None


def current_session() -> Session:
    """Return the session bound to this task, or the process-wide default."""
    global _default
    session = _current.get()
    if session is not None:
        return session
    if _default is None:
        _default = Session()
    return _default


@contextmanager
def use_session(session: Session) -> Iterator[Session]:
    """Bind ``session`` for the duration of the block, including awaited code."""
    token = _current.set(session)
    try:
        yield session
    finally:
        try:
            _current.reset(token)
        except ValueError:
            # Generator finalized in a different context than it started in
            # (threadpool-iterated SSE streams). The context copy that held
            # the token is already gone; there is nothing to reset.
            pass
