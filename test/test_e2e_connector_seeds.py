"""E2E Phase 11: connector seed sweep.

Inspect every MCP server and every "OpenAPI that inspects" row of
``socaity_backend/docs/planned/connector-seeds.md`` without a credential. A seed is
reachable when inspect succeeds, answers ``auth_required`` (the credential HIT the
user would see) or ``connector_exists``. At least 60% must be reachable. Templated
hosts (``{shop}``) are not connectable and are skipped. Inspect writes no catalog row.

    python test/test_e2e_connector_seeds.py
    pytest test/test_e2e_connector_seeds.py -v -s

Keys: see ``agentic_utils``.
"""
from __future__ import annotations

import contextvars
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import agentic_utils as env  # noqa: E402  (sets URL defaults before socaity import)

from socaity import Session, client  # noqa: E402
from socaity_cli.errors import BackendApiError  # noqa: E402

SEEDS_FILE = env.PROJECTS_ROOT / "socaity_backend" / "docs" / "planned" / "connector-seeds.md"
REACHABLE_CODES = {"auth_required", "connector_exists"}
MIN_REACHABLE = 0.6
# (section heading that opens the table, column holding the connect URL)
SEED_TABLES = (("# MCP servers", 0), ("## OpenAPI that inspects", -1))
_URL = re.compile(r"`(https?://[^`]+)`")

pytestmark = [
    pytest.mark.skipif(not env.backend_up(), reason=f"backend not reachable at {env.BACKEND}"),
    pytest.mark.skipif(not env.api_key(), reason=env.missing_env("SOCAITY_API_KEY") or "no SOCAITY_API_KEY"),
]


def seed_urls() -> list[str]:
    """Connect URLs of the seed tables, in file order."""
    urls: list[str] = []
    column = None
    for line in SEEDS_FILE.read_text(encoding="utf-8").splitlines():
        if line.startswith("#"):
            column = next((col for heading, col in SEED_TABLES if line.strip() == heading), None)
        elif column is not None and line.startswith("|"):
            found = _URL.findall(line)
            if found:
                urls.append(found[column])
    return urls


def _probe(url: str) -> str:
    """``ok``, a reachable error code, or the failing code / exception."""
    try:
        client.inspect_connector(url)
        return "ok"
    except BackendApiError as exc:
        return exc.code or f"http_{exc.status_code}"
    except Exception as exc:
        return type(exc).__name__


def run() -> None:
    urls = seed_urls()
    templated = [url for url in urls if "{" in url]
    connectable = [url for url in urls if "{" not in url]
    with Session(api_key=env.api_key(), backend_url=env.BACKEND), ThreadPoolExecutor(max_workers=8) as pool:
        # The session lives in a ContextVar; worker threads only see it through a copy taken here.
        contexts = [contextvars.copy_context() for _ in connectable]
        outcomes = list(pool.map(lambda ctx, url: ctx.run(_probe, url), contexts, connectable))

    reachable = [url for url, outcome in zip(connectable, outcomes) if outcome == "ok" or outcome in REACHABLE_CODES]
    for url, outcome in zip(connectable, outcomes):
        env.log("T11", f"{outcome:<24} {url}")
    ratio = len(reachable) / len(connectable)
    env.log("T11", f"reachable={len(reachable)}/{len(connectable)} ({ratio:.0%}) skipped templated={templated}")
    assert ratio >= MIN_REACHABLE, f"only {ratio:.0%} of connector seeds reach inspect or a credential HIT"
    env.log("T11", "PASS")


def test_connector_seed_sweep() -> None:
    run()


if __name__ == "__main__":
    run()
