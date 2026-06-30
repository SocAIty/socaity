import json
from pathlib import Path

from socaity.core import credentials as creds


def _use_config_dir(tmp_path: Path):
    creds.config_dir = lambda: tmp_path / "socaity"


def test_credentials_roundtrip(tmp_path):
    _use_config_dir(tmp_path)
    saved = creds.Credentials(
        api_key="tk_test_key",
        user_id="uid-1",
        user_email="dev@socaity.ai",
        backend_url="https://webapi.socaity.ai",
    )
    creds.save_credentials(saved)

    loaded = creds.load_credentials()
    assert loaded is not None
    assert loaded.api_key == "tk_test_key"
    assert loaded.user_email == "dev@socaity.ai"

    data = json.loads((tmp_path / "socaity" / "credentials.json").read_text())
    assert data["api_key"] == "tk_test_key"


def test_clear_credentials(tmp_path):
    _use_config_dir(tmp_path)
    creds.save_credentials(creds.Credentials(api_key="tk_x"))
    assert creds.clear_credentials() is True
    assert creds.load_credentials() is None


if __name__ == "__main__":
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        test_credentials_roundtrip(root)
        test_clear_credentials(root)
    print("credentials tests passed")
