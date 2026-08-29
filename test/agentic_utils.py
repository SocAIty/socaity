"""Shared plumbing for the SPAINE agent / workflow e2e tests.

These tests need the local platform stack: socaity_backend (:8000), the
inference gateway + orchestrator + engines (:8001), and the SPAINE agent in
the catalog. Import this module before ``socaity`` so the URL defaults land
first.

Credentials: ``SOCAITY_TEST_RICH_KEY`` / ``SOCAITY_TEST_POOR_KEY`` env vars,
else the SPAINE dev keys file (``SPAINE_KEYS_FILE`` or the sibling
``socaity_backend/agents/SPAINE/second_user_api_keys.txt``), else the regular
``SOCAITY_API_KEY`` for the rich user.
"""
from __future__ import annotations

import os
import time
from pathlib import Path
from typing import Optional

import httpx

os.environ.setdefault("SOCAITY_BACKEND_URL", "http://127.0.0.1:8000")
os.environ.setdefault("INFERENCE_BACKEND_URL", "http://127.0.0.1:8001")

BACKEND = os.environ["SOCAITY_BACKEND_URL"].rstrip("/")
INFERENCE = os.environ["INFERENCE_BACKEND_URL"].rstrip("/")
PROJECTS_ROOT = Path(__file__).resolve().parents[2]
KEYS_FILE = Path(
    os.getenv("SPAINE_KEYS_FILE")
    or PROJECTS_ROOT / "socaity_backend" / "agents" / "SPAINE" / "second_user_api_keys.txt"
)
TERMINAL = ("finished", "failed", "timeout", "cancelled", "rejected")


def _key_from_file(label: str) -> Optional[str]:
    if not KEYS_FILE.is_file():
        return None
    lines = [line.strip() for line in KEYS_FILE.read_text().splitlines()]
    for index, line in enumerate(lines):
        if line.startswith(f"# {label}") and index + 1 < len(lines):
            return lines[index + 1]
    return None


def rich_key() -> Optional[str]:
    """Funded test user (owns the runs)."""
    return os.getenv("SOCAITY_TEST_RICH_KEY") or _key_from_file("Rich") or os.getenv("SOCAITY_API_KEY")


def poor_key() -> Optional[str]:
    """Second, low-credit test user (fork / permission scenarios)."""
    return os.getenv("SOCAITY_TEST_POOR_KEY") or _key_from_file("Poor")


def backend_up() -> bool:
    try:
        return httpx.get(f"{BACKEND}/v1/catalog/services", params={"limit": 1}, timeout=10).status_code == 200
    except httpx.HTTPError:
        return False


def inference_up() -> bool:
    try:
        httpx.get(f"{INFERENCE}/openapi.json", timeout=10)
        return True
    except httpx.HTTPError:
        return False


def poll_job(job_id: str, api_key: str, timeout_s: float = 600) -> dict:
    """Poll gateway ``GET /status/{job_id}`` until terminal."""
    deadline = time.monotonic() + timeout_s
    with httpx.Client(headers={"x-api-key": api_key}, timeout=60) as client:
        while time.monotonic() < deadline:
            response = client.get(f"{INFERENCE}/status/{job_id}")
            if response.status_code == 200:
                envelope = response.json()
                if (envelope.get("status") or "").lower() in TERMINAL:
                    return envelope
            time.sleep(2)
    raise TimeoutError(f"job {job_id} not terminal within {timeout_s}s")


def log(tag: str, msg: str) -> None:
    print(f"[{tag}] {msg}", flush=True)
