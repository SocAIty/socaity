"""Lazy bridge to APIPod CLI (requires ``pip install socaity[apipod]`` or ``pip install apipod``)."""

from __future__ import annotations

import sys
from typing import List, Optional

APIPOD_INSTALL_HINT = (
    "APIPod is required for this command. Install with:\n"
    "  pip install socaity[apipod]\n"
    "or:\n"
    "  pip install apipod"
)


def _ensure_apipod_installed():
    try:
        import apipod.cli  # noqa: F401
    except ImportError as exc:
        print(APIPOD_INSTALL_HINT)
        raise SystemExit(1) from exc


def _run_apipod_argv(argv: List[str]) -> None:
    _ensure_apipod_installed()
    import apipod.cli

    previous = sys.argv
    sys.argv = ["apipod", *argv]
    try:
        apipod.cli.main()
    finally:
        sys.argv = previous


def run_scan() -> None:
    _run_apipod_argv(["--scan"])


def run_build(
    target_file: Optional[str],
    *,
    orchestrator: str,
    compute: str,
    provider: str,
    region: Optional[str],
) -> None:
    argv = ["--build"]
    if target_file:
        argv.append(target_file)
    argv.extend([
        "--orchestrator", orchestrator,
        "--compute", compute,
        "--provider", provider,
    ])
    if region:
        argv.extend(["--region", region])
    _run_apipod_argv(argv)


def run_start(
    *,
    orchestrator: str,
    compute: str,
    provider: str,
    region: Optional[str],
    host: Optional[str],
    port: Optional[int],
) -> None:
    argv = ["--start", "--orchestrator", orchestrator, "--compute", compute, "--provider", provider]
    if region:
        argv.extend(["--region", region])
    if host:
        argv.extend(["--host", host])
    if port is not None:
        argv.extend(["--port", str(port)])
    _run_apipod_argv(argv)
