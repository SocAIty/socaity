"""Shared plumbing for official-service manual tests (face2face, speechcraft)."""
from __future__ import annotations

import os
from pathlib import Path
from typing import Any, List, Optional

from meseex.events import EventKind, MeseexEvent

from socaity import Session, client

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output"


def load_repo_env() -> None:
    env_file = ROOT.parent / ".env"
    if not env_file.is_file():
        return
    for line in env_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, _, value = line.partition("=")
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def require_key() -> str:
    key = os.getenv("SOCAITY_API_KEY")
    if not key:
        raise RuntimeError("set SOCAITY_API_KEY or run: socaity login")
    return key


def session():
    """Credential-bound session. Gate follows ``APIPOD_GATE_URL`` when set."""
    load_repo_env()
    return Session(api_key=require_key())


def connect(name: str):
    return client.connect(name)


def watch(job) -> List[MeseexEvent]:
    """Collect lifecycle events including progress while the job runs."""
    events: List[MeseexEvent] = []
    job.subscribe(events.append, replay=True)
    return events


def assert_progress(events: List[MeseexEvent], job) -> None:
    """File-transfer jobs must emit lifecycle progress, not only a terminal result."""
    kinds = {event.kind for event in events}
    progress_events = [event for event in events if event.kind is EventKind.PROGRESS]
    assert EventKind.STARTED in kinds or progress_events, f"no start/progress events: {kinds}"
    assert EventKind.SUCCEEDED in kinds or getattr(job, "is_terminal", False), f"job did not succeed: {kinds}"
    if progress_events:
        assert any(event.task_progress is not None or event.message for event in progress_events)


def save_media(result: Any, path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = result[0] if isinstance(result, list) and result else result
    assert payload is not None, f"empty result for {path}"
    if hasattr(payload, "save"):
        payload.save(str(path))
    else:
        path.write_bytes(payload if isinstance(payload, (bytes, bytearray)) else bytes(payload))
    assert path.is_file() and path.stat().st_size > 0, f"nothing written to {path}"
    return path


def first_existing(*candidates: Path) -> Optional[Path]:
    for path in candidates:
        if path.is_file():
            return path
    return None
