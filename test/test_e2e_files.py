"""E2E: socaity SDK file_service (malware reject + expires_at + expand).

Requires a running backend with migration 014 applied and yara-x installed.
Point SOCAITY_BACKEND_URL at the backend under test and run:

    pytest test/test_e2e_files.py -v

Or run this file in the IDE (``__main__``).
"""
from datetime import datetime, timedelta, timezone
from pathlib import Path
import os
import sys

import httpx
import pytest


def _load_repo_env() -> None:
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

import socaity  # noqa: E402
from socaity.core.session import current_session  # noqa: E402

BACKEND = os.environ["SOCAITY_BACKEND_URL"]
TEST_FILES = Path(__file__).resolve().parent / "test_files"
MW_PATH = TEST_FILES / "mw-test.txt"
WAV_PATH = TEST_FILES / "audio" / "potter_to_hermine.wav"
if not WAV_PATH.is_file():
    WAV_PATH = TEST_FILES / "potter_to_hermine.wav"


def _backend_up() -> bool:
    try:
        return httpx.get(BACKEND + "v1/catalog/services", params={"limit": 1}, timeout=10).status_code == 200
    except httpx.HTTPError:
        return False


def _has_credentials() -> bool:
    if os.getenv("SOCAITY_API_KEY"):
        return True
    creds = Path.home() / ".config" / "socaity" / "credentials.json"
    return creds.is_file()


def sdk():
    return current_session().client


pytestmark = [
    pytest.mark.skipif(not _backend_up(), reason=f"backend not reachable at {BACKEND}"),
    pytest.mark.skipif(not _has_credentials(), reason="no SOCAITY_API_KEY or CLI credentials"),
]


def test_malware_upload_rejected():
    assert MW_PATH.is_file(), f"missing malware fixture: {MW_PATH}"
    with pytest.raises(httpx.HTTPStatusError) as exc_info:
        sdk().upload_files(MW_PATH, purpose="USER_UPLOAD")
    response = exc_info.value.response
    assert response.status_code == 400
    body = response.text
    assert "FILE_MALWARE" in body


@pytest.mark.skipif(not WAV_PATH.is_file(), reason=f"missing wav fixture: {WAV_PATH}")
def test_upload_wav_sets_expires_at_and_expand_references():
    expires_at = (datetime.now(timezone.utc) + timedelta(hours=24)).isoformat()
    rows = sdk().upload_files(WAV_PATH, purpose="USER_UPLOAD", expires_at=expires_at)
    assert rows, "upload returned no file records"
    uploaded = rows[0]
    assert uploaded.get("id") is not None
    assert uploaded.get("expires_at")

    fetched = sdk().get_file(uploaded["id"], expand=["references"])
    assert fetched is not None
    assert fetched.get("id") == uploaded["id"]
    assert fetched.get("expires_at")
    refs = fetched.get("references") or []
    assert refs, "expand=references returned no file_references"
    assert any(ref.get("purpose") == "USER_UPLOAD" for ref in refs)


def test_storage_usage_and_permanent_upload():
    """Quota RPC + a keep-file upload (expires_at null). Cleans up the uploaded row."""
    usage = sdk().get_storage_usage()
    assert usage is not None
    assert usage.get("user_id")
    assert int(usage["storage_space_bytes"]) > 0
    assert int(usage["free_storage_bytes"]) >= 0

    tmp = Path(__file__).resolve().parent / "test_files" / "_phase0_keep.txt"
    tmp.write_text("phase0 permanent upload probe\n", encoding="utf-8")
    try:
        rows = sdk().upload_files(tmp, purpose="USER_UPLOAD")
        assert rows, "permanent upload returned no file records"
        uploaded = rows[0]
        assert uploaded.get("id") is not None
        assert uploaded.get("expires_at") in (None, "")
        after = sdk().get_storage_usage()
        assert int(after["used_storage_bytes"]) >= int(usage["used_storage_bytes"])
        assert sdk().delete_file(uploaded["id"]) is True
    finally:
        tmp.unlink(missing_ok=True)


if __name__ == "__main__":
    failures = 0
    for name, fn in (
        ("test_malware_upload_rejected", test_malware_upload_rejected),
        ("test_upload_wav_sets_expires_at_and_expand_references", test_upload_wav_sets_expires_at_and_expand_references),
        ("test_storage_usage_and_permanent_upload", test_storage_usage_and_permanent_upload),
    ):
        if name.startswith("test_upload") and not WAV_PATH.is_file():
            print(f"SKIP {name}: missing {WAV_PATH}")
            continue
        try:
            fn()
            print(f"PASS {name}")
        except Exception as exc:
            failures += 1
            print(f"FAIL {name}: {exc}")
    sys.exit(1 if failures else 0)
