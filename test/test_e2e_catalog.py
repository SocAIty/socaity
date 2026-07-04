"""E2E: socaity SDK against a running backend (catalog, search, CLI, connect).

Point SOCAITY_BACKEND_URL at the backend under test (default local dev
backend with its typesense sidecar) and run:

    pytest test/test_e2e_catalog.py -v

The image-generation test calls flux-schnell through the inference gateway
and needs valid credentials (socaity login or SOCAITY_API_KEY).
"""
import io
import os
import sys
from pathlib import Path

import httpx
import pytest


def _load_repo_env() -> None:
    """Pick up the repo's .env (API keys); explicit env vars still win."""
    env_file = Path(__file__).resolve().parents[1] / ".env"
    if not env_file.is_file():
        return
    for line in env_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, _, value = line.partition("=")
            os.environ.setdefault(key.strip(), value.strip().strip('"'))


_load_repo_env()
os.environ.setdefault("SOCAITY_BACKEND_URL", "http://127.0.0.1:8000/")

import socaity  # noqa: E402  (env must be set before the client is built)
from socaity.cli import main as cli_main  # noqa: E402

BACKEND = os.environ["SOCAITY_BACKEND_URL"]


def _backend_up() -> bool:
    try:
        return httpx.get(BACKEND + "v1/catalog/services", params={"limit": 1}, timeout=10).status_code == 200
    except httpx.HTTPError:
        return False


pytestmark = pytest.mark.skipif(not _backend_up(), reason=f"backend not reachable at {BACKEND}")


# ---------------------------------------------------------------- catalog

def test_list_services_slim_and_lazy():
    services = socaity.list_services(limit=5)
    assert services, "catalog returned no services"

    slim = services[0].raw
    assert slim.id and slim.name
    assert not slim.deployments, "list view should be slim (no relations)"

    # First relation access hydrates the full record through one fetch.
    deployments = services[0].deployments
    assert deployments and deployments[0].provider


def test_get_service_full():
    name = socaity.list_services(limit=1)[0].raw.name
    service = socaity.get_service(name)
    assert service.name == name
    assert service.deployments and service.endpoints


def test_pagination_no_overlap():
    page1 = {s.raw.id for s in socaity.list_services(limit=3, offset=0)}
    page2 = {s.raw.id for s in socaity.list_services(limit=3, offset=3)}
    assert len(page1) == 3
    assert not page1 & page2


def test_sparse_fieldsets_wire_shape():
    """The raw HTTP response must only carry the selected fields."""
    rows = httpx.get(
        BACKEND + "v1/catalog/services",
        params={"limit": 2, "select": "id,name"},
        timeout=30,
    ).json()
    assert rows and all(set(row.keys()) <= {"id", "name"} for row in rows)


def test_list_and_get_models():
    models = socaity.list_models(limit=10)
    assert models, "no AIModels in catalog; run the scraping pipeline first"
    model = socaity.get_model(models[0].name)
    assert model and model.id == models[0].id


def test_list_categories():
    categories = socaity.list_categories()
    assert categories and all(c.id for c in categories)


# ---------------------------------------------------------------- search

def test_search_typo_tolerant():
    hits = socaity.search("flux schnel", collections="services", limit=5)
    names = [hit["document"].get("name", "") for hit in hits]
    assert any("flux-schnell" in name for name in names), names


def test_search_models_collection():
    hits = socaity.search("deepseek", collections="models", limit=5)
    assert hits and all(hit["collection"] == "models" for hit in hits)


# ---------------------------------------------------------------- CLI

def _run_cli(*argv: str) -> str:
    buffer = io.StringIO()
    stdout, sys.stdout = sys.stdout, buffer
    try:
        cli_main(list(argv))
    finally:
        sys.stdout = stdout
    return buffer.getvalue()


def test_cli_list_services():
    output = _run_cli("list", "services", "--limit", "3")
    assert len(output.strip().splitlines()) == 3


def test_cli_list_models():
    output = _run_cli("list", "models", "--limit", "3")
    assert "No models found." not in output


def test_cli_search():
    output = _run_cli("search", "flux schnel", "--limit", "3")
    assert "flux-schnell" in output or "flux schnell" in output.lower()


# ---------------------------------------------------------------- connect

@pytest.mark.skipif(not os.getenv("SOCAITY_API_KEY") and not os.path.exists(
    os.path.join(os.path.expanduser("~"), ".config", "socaity", "credentials.json")),
    reason="no credentials for inference")
def test_connect_flux_schnell_creates_image(tmp_path):
    client = socaity.connect("black-forest-labs-flux-schnell")
    job = client.submit_job("/predictions", prompt="a lighthouse on a cliff at sunset, watercolor")
    result = job.get_result()
    assert result is not None

    saved = tmp_path / "flux_schnell.png"
    if hasattr(result, "save"):
        result.save(str(saved))
    else:
        saved.write_bytes(result if isinstance(result, bytes) else bytes(result))
    assert saved.stat().st_size > 10_000, "image suspiciously small"
