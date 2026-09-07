"""Credential-scoped access to the socaity backend.

Hosts that serve several callers from one process (the MCP server, SPAINE)
open one session per request. The session lives in a ``ContextVar``, so
concurrent tasks cannot observe or reuse each other's credentials. Scripts
and notebooks use the process-wide default session.

The package-level ``client`` object forwards to the active session's
``Client``. Explicit ``Client(...)`` handles ignore the ContextVar.
"""
from __future__ import annotations

from contextvars import ContextVar, Token
from pathlib import Path
from typing import List, Optional

from socaity.client import DEFAULT_APIPOD_GATE_URL, SocaityClient

DEFAULT_APIPOD_GATE_URL = DEFAULT_APIPOD_GATE_URL


class Session:
    """One caller's credentials plus the ``Client`` bound to them.

    Use as a context manager to switch the active ``client``:

        with Session(api_key=key):
            client.run_service(...)

    Args:
        api_key: Socaity API key. ``None`` falls back to ``SOCAITY_API_KEY`` or
            the credentials written by ``socaity login``.
        backend_url: Override the backend base URL (tests, self-hosted).
        materialize_media: Default for clients created through ``connect``.
            ``False`` keeps file results as URL references.
        user_id: Caller id when the host already knows it (SPAINE, MCP).
        user_name: Display name for prompts. Never send ``api_key`` to a model.
        conversation_id: Current chat id, if the host has one.
        local_root: User-local sandbox root on the host.
        gate_url: APIPod gate origin for factory jobs (agent chat, workflow run).
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
        gate_url: Optional[str] = None,
    ):
        self.client = SocaityClient(
            api_key=api_key,
            backend_url=backend_url,
            gate_url=gate_url,
            materialize_media=materialize_media,
        )
        self.api_key = self.client.api_key
        self.materialize_media = materialize_media
        self.user_id = user_id
        self.user_name = user_name
        self.conversation_id = conversation_id
        self.local_root = local_root
        self.gate_url = self.client.gate_url
        self._tokens: List[Token] = []

    def __enter__(self) -> Session:
        self._tokens.append(_current.set(self))
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        if not self._tokens:
            return
        token = self._tokens.pop()
        try:
            _current.reset(token)
        except ValueError:
            # Generator finalized in a different context than it started in
            # (threadpool-iterated SSE streams). The context copy that held
            # the token is already gone; there is nothing to reset.
            pass


class ActiveClient:
    """Forwards attribute access to the ``Client`` of the active session."""

    def __getattr__(self, name: str):
        return getattr(current_session().client, name)

    def __dir__(self) -> List[str]:
        return sorted(set(dir(type(self))) | set(dir(current_session().client)))

    def __repr__(self) -> str:
        return f"<ActiveClient of {current_session().client!r}>"


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
