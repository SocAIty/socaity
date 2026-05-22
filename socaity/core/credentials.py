"""XDG credentials storage for the Socaity CLI."""

from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

DEFAULT_BACKEND_URL = "https://webapi.socaity.ai"
DEFAULT_FRONTEND_URL = "https://wonderful-wave-0a392ca03.2.azurestaticapps.net/"

_LEGACY_TOKEN_FILE = Path.home() / ".apipod" / "token"


@dataclass
class Credentials:
    api_key: str
    user_id: Optional[str] = None
    user_email: Optional[str] = None
    backend_url: str = DEFAULT_BACKEND_URL
    logged_in_at: Optional[str] = None

    def apply_to_env(self) -> None:
        os.environ["SOCAITY_API_KEY"] = self.api_key
        os.environ["SOCAITY_BACKEND_URL"] = self.backend_url.rstrip("/") + "/"


def config_dir() -> Path:
    xdg = os.environ.get("XDG_CONFIG_HOME", "").strip()
    base = Path(xdg) if xdg else Path.home() / ".config"
    return base / "socaity"


def credentials_path() -> Path:
    return config_dir() / "credentials.json"


def load_credentials() -> Optional[Credentials]:
    path = credentials_path()
    if path.is_file():
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            api_key = (data.get("api_key") or "").strip()
            if api_key:
                return Credentials(
                    api_key=api_key,
                    user_id=data.get("user_id"),
                    user_email=data.get("user_email"),
                    backend_url=(data.get("backend_url") or DEFAULT_BACKEND_URL).rstrip("/"),
                    logged_in_at=data.get("logged_in_at"),
                )
        except (json.JSONDecodeError, OSError):
            pass

    legacy = _load_legacy_token()
    if legacy:
        save_credentials(legacy)
        return legacy
    return None


def _load_legacy_token() -> Optional[Credentials]:
    if not _LEGACY_TOKEN_FILE.is_file():
        return None
    try:
        token = _LEGACY_TOKEN_FILE.read_text(encoding="utf-8").strip()
        if not token:
            return None
        backend = os.environ.get("SOCAITY_BACKEND_URL", DEFAULT_BACKEND_URL).rstrip("/")
        return Credentials(
            api_key=token,
            backend_url=backend,
            logged_in_at=datetime.now(timezone.utc).isoformat(),
        )
    except OSError:
        return None


def save_credentials(credentials: Credentials) -> Path:
    directory = config_dir()
    directory.mkdir(parents=True, exist_ok=True)
    path = credentials_path()
    payload: dict[str, Any] = asdict(credentials)
    payload["backend_url"] = credentials.backend_url.rstrip("/")
    if not payload.get("logged_in_at"):
        payload["logged_in_at"] = datetime.now(timezone.utc).isoformat()
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    path.chmod(0o600)
    credentials.apply_to_env()
    return path


def clear_credentials() -> bool:
    path = credentials_path()
    if path.is_file():
        path.unlink()
        return True
    return False


def get_api_key() -> Optional[str]:
    creds = load_credentials()
    if creds:
        creds.apply_to_env()
        return creds.api_key
    env_key = os.environ.get("SOCAITY_API_KEY", "").strip()
    return env_key or None


def require_credentials() -> Credentials:
    creds = load_credentials()
    if creds:
        creds.apply_to_env()
        return creds
    print("Not logged in. Run: socaity login")
    raise SystemExit(1)
