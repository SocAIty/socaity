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
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        backend_url: Optional[str] = None,
        materialize_media: bool = True,
    ):
        self.api_key = api_key
        self.materialize_media = materialize_media
        self.backend = SocaityBackendClient(backend_url=backend_url, api_key=api_key)


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
        _current.reset(token)
