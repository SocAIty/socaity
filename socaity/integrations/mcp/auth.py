"""Resolve and refresh API credentials for MCP tools (same store as the CLI)."""
from __future__ import annotations

import os
from typing import Any, Dict, Optional

from socaity_cli.auth import fetch_profile, run_login
from socaity_cli.credentials import (
    Credentials,
    get_api_key,
    load_credentials,
)


def ensure_api_key() -> str:
    """Return the active API key or raise if neither env nor credentials exist."""
    key = (get_api_key() or "").strip()
    if key:
        os.environ.setdefault("SOCAITY_API_KEY", key)
        return key
    raise RuntimeError(
        "Not authenticated. Call the login tool (browser device flow) or set SOCAITY_API_KEY."
    )


def whoami() -> Dict[str, Any]:
    key = ensure_api_key()
    creds = load_credentials()
    backend = (creds.backend_url if creds else None) or os.environ.get(
        "SOCAITY_BACKEND_URL", "https://webapi.socaity.ai"
    )
    backend = backend.rstrip("/")
    email = creds.user_email if creds else None
    user_id = creds.user_id if creds else None
    if not email or not user_id:
        profile = fetch_profile(api_key=key, backend_url=backend)
        email = email or profile.get("email") or profile.get("user_email")
        user_id = user_id or profile.get("id") or profile.get("user_id")
    return {
        "user_id": user_id,
        "email": email,
        "backend_url": backend,
        "api_key_prefix": (key[:6] + "…") if key else None,
    }


def login(*, no_browser: bool = False, timeout: int = 300) -> Dict[str, Any]:
    """Open the CLI login flow and persist a temporary ``tk_`` key."""
    try:
        creds: Credentials = run_login(no_browser=no_browser, timeout=timeout)
    except SystemExit as exc:
        raise RuntimeError("Login failed or timed out. Retry login or set SOCAITY_API_KEY.") from exc
    creds.apply_to_env()
    return {
        "status": "ok",
        "user_id": creds.user_id,
        "email": creds.user_email,
        "backend_url": creds.backend_url,
    }


def current_credentials() -> Optional[Credentials]:
    return load_credentials()
