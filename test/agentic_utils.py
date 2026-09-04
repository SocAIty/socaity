"""Shared plumbing for the SPAINE agent / workflow e2e tests.

These tests need the local platform stack: socaity_backend (:8000), the
inference gateway + orchestrator + engines, and SPAINE in the catalog.
Import this module before ``socaity`` so the URL defaults land first.

Credentials are env-only: ``SOCAITY_TEST_RICH_KEY`` / ``SOCAITY_TEST_POOR_KEY``,
else ``SOCAITY_API_KEY`` for the rich user. Gate origin is ``APIPOD_GATE_URL``.
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

import httpx


_CRED_KEYS = ("SOCAITY_API_KEY", "SOCAITY_TEST_RICH_KEY", "SOCAITY_TEST_POOR_KEY")


def _load_repo_env() -> None:
    """Load test credentials from the SDK .env. Do not inherit cloud URLs."""
    env_file = Path(__file__).resolve().parents[1] / ".env"
    if not env_file.is_file():
        return
    for line in env_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, _, value = line.partition("=")
            name = key.strip()
            if name in _CRED_KEYS:
                os.environ.setdefault(name, value.strip().strip('"').strip("'"))


_load_repo_env()
os.environ["SOCAITY_BACKEND_URL"] = "http://127.0.0.1:8000"
os.environ["APIPOD_GATE_URL"] = "http://127.0.0.1:8001"

BACKEND = os.environ["SOCAITY_BACKEND_URL"].rstrip("/")
GATE = os.environ["APIPOD_GATE_URL"].rstrip("/")
TERMINAL = ("finished", "failed", "timeout", "cancelled", "rejected")
PROJECTS_ROOT = Path(__file__).resolve().parents[2]


def rich_key() -> Optional[str]:
    """Funded test user (owns the runs)."""
    return os.getenv("SOCAITY_TEST_RICH_KEY") or os.getenv("SOCAITY_API_KEY")


def poor_key() -> Optional[str]:
    """Second, low-credit test user (fork / permission scenarios)."""
    return os.getenv("SOCAITY_TEST_POOR_KEY")


def backend_up() -> bool:
    try:
        return httpx.get(f"{BACKEND}/v1/catalog/services", params={"limit": 1}, timeout=10).status_code == 200
    except httpx.HTTPError:
        return False


def inference_up() -> bool:
    try:
        httpx.get(f"{GATE}/openapi.json", timeout=10)
        return True
    except httpx.HTTPError:
        return False


def poll_job(job_id: str, api_key: Optional[str] = None, timeout_s: float = 600) -> dict:
    """Wait until the gateway job is terminal. Uses the SDK wait helper."""
    from socaity.tools.jobs import wait_for_job

    _ = api_key
    return wait_for_job(job_id, timeout_s=timeout_s)


def log(tag: str, msg: str) -> None:
    print(f"[{tag}] {msg}", flush=True)
