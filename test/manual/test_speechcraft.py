"""Manual: official speechcraft through ``client.connect`` / ``submit_job``.

Checks file transfer (wav in, audio out), job progress events, and
byte streaming on ``/text2voice`` with ``stream=True``. Not part of the
default pytest suite.

    python test/manual/test_speechcraft.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

from socaity import MediaFile

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _support import (  # noqa: E402
    OUTPUT,
    ROOT,
    assert_progress,
    connect,
    first_existing,
    save_media,
    session,
    watch,
)

pytestmark = pytest.mark.manual

OUT = OUTPUT / "speechcraft"
SAMPLE = "I love society [laughs]! [happy] What a day to make voice overs with artificial intelligence."
CLONE_1 = first_existing(
    ROOT / "test_files" / "text2speech" / "voice_clone_test_voice_1.wav",
    ROOT / "test_files" / "audio" / "voice_clone_test_voice_1.wav",
)
CLONE_2 = first_existing(
    ROOT / "test_files" / "text2speech" / "voice_clone_test_voice_2.wav",
    ROOT / "test_files" / "audio" / "voice_clone_test_voice_2.wav",
)


def _text2voice():
    job = connect("speechcraft").submit_job("/text2voice", text=SAMPLE, voice="hermine")
    events = watch(job)
    audio = job.get_result()
    assert_progress(events, job)
    save_media(audio, OUT / "hermine_i_love_socaity.wav")
    return audio


def _text2voice_stream():
    """Consume the live audio byte stream instead of assembling after the fact."""
    job = connect("speechcraft").submit_job(
        "/text2voice",
        text=SAMPLE,
        voice="hermine",
        stream=True,
    )
    events = watch(job)
    session_stream = job.stream()
    nbytes = 0
    try:
        for chunk in session_stream.iter_bytes():
            nbytes += len(chunk)
    finally:
        closer = getattr(session_stream, "close", None)
        if closer:
            closer()
    assert nbytes > 0, "streamed text2voice produced no bytes"
    assert_progress(events, job)
    print(f"[speechcraft] streamed {nbytes} bytes")
    return nbytes


def _voice2embedding():
    if CLONE_1 is None:
        raise FileNotFoundError("missing voice clone wav under test_files/text2speech")
    job = connect("speechcraft").submit_job(
        "/voice2embedding",
        audio_file=str(CLONE_1),
        voice_name="hermine",
        save=False,
    )
    events = watch(job)
    embedding = job.get_result()
    assert embedding is not None
    assert_progress(events, job)
    save_media(embedding, OUT / "hermine_embedding.wav")
    return embedding


def _text2voice_with_embedding():
    path = OUT / "hermine_embedding.wav"
    if not path.is_file():
        _voice2embedding()
    voice = MediaFile().from_file(str(path))
    job = connect("speechcraft").submit_job("/text2voice", text=SAMPLE, voice=voice)
    events = watch(job)
    audio = job.get_result()
    assert_progress(events, job)
    save_media(audio, OUT / "hermine_cloned.wav")
    return audio


def _voice2voice():
    if CLONE_2 is None:
        raise FileNotFoundError("missing voice2voice wav under test_files/text2speech")
    job = connect("speechcraft").submit_job(
        "/voice2voice",
        audio_file=str(CLONE_2),
        voice_name="hermine",
    )
    events = watch(job)
    audio = job.get_result()
    assert audio is not None
    assert_progress(events, job)
    save_media(audio, OUT / "benni.wav")
    return audio


def run() -> None:
    with session():
        print("[speechcraft] text2voice (progress + file out)")
        _text2voice()
        print("[speechcraft] text2voice stream=True (byte stream)")
        _text2voice_stream()
        if CLONE_1 is not None:
            print("[speechcraft] voice2embedding + cloned text2voice")
            _text2voice_with_embedding()
        else:
            print("[speechcraft] skip clone, missing reference wav")
        if CLONE_2 is not None:
            print("[speechcraft] voice2voice")
            _voice2voice()
        else:
            print("[speechcraft] skip voice2voice, missing second wav")
    print("[speechcraft] PASS")


if __name__ == "__main__":
    run()
