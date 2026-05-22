"""Browser-based CLI login (device authorization flow via web UI)."""

from __future__ import annotations

import os
import shutil
import subprocess
import time
import webbrowser
from typing import Any, Dict, Optional
from urllib.parse import urljoin

import httpx

from socaity.core.credentials import (
    Credentials,
    DEFAULT_BACKEND_URL,
    DEFAULT_FRONTEND_URL,
    save_credentials,
)

USER_AGENT = "socaity-cli/0.1.10"


def _backend_base_url() -> str:
    return os.environ.get("SOCAITY_BACKEND_URL", DEFAULT_BACKEND_URL).rstrip("/")


def _frontend_base_url() -> str:
    return os.environ.get("SOCAITY_FRONTEND_URL", DEFAULT_FRONTEND_URL).rstrip("/")


def _web_api_url(base: str) -> str:
    return urljoin(base + "/", "v1/")


def open_login_url(url: str) -> bool:
    try:
        if webbrowser.open(url):
            return True
    except Exception:
        pass
    for cmd in ("wslview", "xdg-open"):
        exe = shutil.which(cmd)
        if not exe:
            continue
        try:
            subprocess.run(
                [exe, url],
                check=False,
                timeout=8,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            return True
        except Exception:
            continue
    return False


def start_cli_login(
    *,
    backend_url: Optional[str] = None,
    frontend_url: Optional[str] = None,
    expires_in_seconds: int = 600,
) -> Dict[str, Any]:
    base = (backend_url or _backend_base_url()).rstrip("/")
    payload: Dict[str, Any] = {"expires_in_seconds": expires_in_seconds}
    frontend = (frontend_url or _frontend_base_url()).strip()
    if frontend:
        payload["frontend_base_url"] = frontend.rstrip("/")
    with httpx.Client(timeout=20.0) as client:
        response = client.post(
            _web_api_url(base) + "cli-auth/start",
            json=payload,
            headers={"User-Agent": USER_AGENT},
        )
        response.raise_for_status()
        return response.json()


def poll_cli_login(
    *,
    request_id: str,
    poll_code: str,
    backend_url: Optional[str] = None,
) -> Dict[str, Any]:
    base = (backend_url or _backend_base_url()).rstrip("/")
    with httpx.Client(timeout=20.0) as client:
        response = client.post(
            _web_api_url(base) + "cli-auth/poll",
            json={"request_id": request_id, "poll_code": poll_code},
            headers={"User-Agent": USER_AGENT},
        )
        response.raise_for_status()
        return response.json()


def fetch_profile(*, api_key: str, backend_url: str) -> Dict[str, Any]:
    base = backend_url.rstrip("/")
    with httpx.Client(timeout=20.0) as client:
        response = client.get(
            _web_api_url(base) + "profile/profile",
            headers={
                "Authorization": f"Bearer {api_key}",
                "User-Agent": USER_AGENT,
            },
        )
        response.raise_for_status()
        return response.json()


def run_login(
    *,
    no_browser: bool = False,
    timeout: int = 300,
    backend_url: Optional[str] = None,
    frontend_url: Optional[str] = None,
) -> Credentials:
    base = (backend_url or _backend_base_url()).rstrip("/")
    frontend = (frontend_url or _frontend_base_url()).rstrip("/")

    print("Login to Socaity")
    session = start_cli_login(
        backend_url=base,
        frontend_url=frontend,
    )
    verification_uri = session["verification_uri"]
    request_id = session["request_id"]
    poll_code = session["poll_code"]
    interval = max(int(session.get("interval_seconds", 2)), 1)

    print(f"Open this URL to authenticate:\n{verification_uri}")

    if not no_browser:
        if open_login_url(verification_uri):
            print("Browser opened for login.")
        else:
            print("Could not open a browser automatically. Open the URL manually.")

    print("Waiting for login confirmation...")
    deadline = time.time() + max(timeout, 10)

    while time.time() < deadline:
        poll_response = poll_cli_login(
            request_id=request_id,
            poll_code=poll_code,
            backend_url=base,
        )
        status = poll_response.get("status")

        if status == "pending":
            time.sleep(interval)
            continue
        if status == "expired":
            print("Login request expired. Run: socaity login")
            raise SystemExit(1)
        if status == "approved":
            api_key = (poll_response.get("api_key") or "").strip()
            if not api_key:
                print("Login failed: missing API key in response.")
                raise SystemExit(1)
            creds = Credentials(
                api_key=api_key,
                user_id=poll_response.get("user_id"),
                user_email=poll_response.get("user_email"),
                backend_url=base,
            )
            path = save_credentials(creds)
            email = creds.user_email or "user"
            print(f"Logged in as {email}")
            print(f"Credentials saved to {path}")
            return creds

        print(f"Login failed: unexpected status '{status}'")
        raise SystemExit(1)

    print("Login timed out. Run: socaity login")
    raise SystemExit(1)


def run_whoami() -> None:
    from socaity.core.credentials import require_credentials

    creds = require_credentials()
    email = creds.user_email
    user_id = creds.user_id
    if not email or not user_id:
        try:
            profile = fetch_profile(api_key=creds.api_key, backend_url=creds.backend_url)
            email = email or profile.get("email") or profile.get("user_email")
            user_id = user_id or profile.get("id") or profile.get("user_id")
        except Exception as exc:
            print(f"Could not fetch profile: {exc}")
            raise SystemExit(1) from exc
    print(f"user_id: {user_id}")
    print(f"email: {email}")
    print(f"backend: {creds.backend_url}")
