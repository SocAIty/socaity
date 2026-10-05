"""Collection rules: default pytest skips the Replicate path unless named."""
from pathlib import Path


def pytest_ignore_collect(collection_path, config):
    path = Path(collection_path)
    if path.name == "test_replicate.py":
        return not any("test_replicate" in str(arg) for arg in config.args)
    return None
