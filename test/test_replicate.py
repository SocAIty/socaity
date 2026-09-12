"""Platform-mediated Replicate services through ``client.run_service``.

Separate path from the core stack: these jobs go Replicate via the gateway,
not official hosted APIPod services. Not collected by default pytest
(``-m not replicate``). Run explicitly:

    pytest test/test_replicate.py -m replicate -v -s
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import agentic_utils as env  # noqa: E402

from socaity import Session, client  # noqa: E402

FLUX = "black-forest-labs-flux-schnell"
DEEPSEEK = "deepseek-ai-deepseek-v3"
WHISPER = "vaibhavs10-incredibly-fast-whisper"
AUDIO = Path(__file__).resolve().parent / "test_files" / "audio" / "potter_to_hermine.wav"
if not AUDIO.is_file():
    AUDIO = Path(__file__).resolve().parent / "test_files" / "potter_to_hermine.wav"

pytestmark = [
    pytest.mark.replicate,
    pytest.mark.skipif(not env.backend_up(), reason=f"backend not reachable at {env.BACKEND}"),
    pytest.mark.skipif(not env.inference_up(), reason=f"APIPod gate not reachable at {env.GATE}"),
    pytest.mark.skipif(not env.api_key(), reason=env.missing_env("SOCAITY_API_KEY") or "no SOCAITY_API_KEY"),
]


def _result(service: str, endpoint: str, params: dict, timeout_s: float = 600):
    job = client.run_service(service, endpoint, params)
    payload = job.get_result(timeout_s=timeout_s)
    assert payload is not None, f"{service}{endpoint} returned no result"
    assert job.platform_job_id, f"{service} produced no platform job id"
    return payload


def test_flux_schnell_image() -> None:
    images = _result(
        FLUX,
        "/predictions",
        {
            "prompt": "a lighthouse on a cliff at sunset, watercolor, replicate-e2e",
            "num_outputs": 1,
            "output_format": "png",
        },
    )
    first = images[0] if isinstance(images, list) else images
    assert first is not None


def test_deepseek_v3_text() -> None:
    text = _result(
        DEEPSEEK,
        "/predictions",
        {"prompt": "Reply with the single word pong and nothing else."},
    )
    blob = text if isinstance(text, str) else str(text)
    assert blob.strip(), "deepseek returned empty text"


@pytest.mark.skipif(not AUDIO.is_file(), reason=f"missing wav fixture: {AUDIO}")
def test_whisper_transcribe() -> None:
    text = _result(
        WHISPER,
        "/predictions",
        {"audio": str(AUDIO)},
        timeout_s=300,
    )
    blob = text if isinstance(text, str) else str(text)
    assert blob.strip(), "whisper returned empty transcript"


def run() -> None:
    session = Session(api_key=env.api_key(), backend_url=env.BACKEND)
    with session:
        env.log("replicate", "flux-schnell")
        test_flux_schnell_image()
        env.log("replicate", "deepseek-v3")
        test_deepseek_v3_text()
        if AUDIO.is_file():
            env.log("replicate", "whisper")
            test_whisper_transcribe()
    env.log("replicate", "PASS")


if __name__ == "__main__":
    run()
