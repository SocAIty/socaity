"""Manual: official face2face through ``client.connect`` / ``submit_job``.

Checks file transfer (local images/video in, media out), job progress
events, and a video result. Not part of the default pytest suite.

    python test/manual/test_face2face.py
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
    save_media,
    session,
    watch,
)

pytestmark = pytest.mark.manual

INPUT = ROOT / "test_files" / "face2face"
OUT = OUTPUT / "face2face"
FACE_1 = INPUT / "test_face_1.jpg"
FACE_2 = INPUT / "test_face_2.jpg"
VIDEO = INPUT / "test_video_ultra_short.mp4"


def _swap_img():
    job = connect("face2face").submit_job(
        "/swap-img-to-img",
        source_img=str(FACE_1),
        target_img=str(FACE_2),
        enhance_face_model=None,
    )
    events = watch(job)
    result = job.get_result()
    assert_progress(events, job)
    save_media(result, OUT / "swap_img.jpg")
    return result


def _embedding():
    job = connect("face2face").submit_job(
        "/add-face",
        face_name="hagrid",
        image=str(FACE_1),
        save=False,
    )
    events = watch(job)
    vector = job.get_result()
    assert vector is not None
    assert_progress(events, job)
    save_media(vector, OUT / "hagrid.npy")
    return vector


def _swap_with_embedding():
    path = OUT / "hagrid.npy"
    if not path.is_file():
        _embedding()
    faces = MediaFile().from_file(str(path))
    job = connect("face2face").submit_job(
        "/swap",
        media=str(FACE_2),
        faces=faces,
        enhance_face_model="gpen_bfr",
    )
    events = watch(job)
    result = job.get_result()
    assert_progress(events, job)
    save_media(result, OUT / "swap_embedded.jpg")
    return result


def _swap_video():
    path = OUT / "hagrid.npy"
    if not path.is_file():
        _embedding()
    faces = MediaFile().from_file(str(path))
    job = connect("face2face").submit_job(
        "/swap-video",
        faces=faces,
        target_video=str(VIDEO),
        include_audio=True,
        enhance_face_model="gpen_bfr_512",
    )
    events = watch(job)
    result = job.get_result()
    assert result is not None
    assert_progress(events, job)
    save_media(result, OUT / "swapped_video.mp4")
    return result


def run() -> None:
    if not FACE_1.is_file() or not FACE_2.is_file():
        raise FileNotFoundError(f"missing face fixtures under {INPUT}")
    with session():
        print("[face2face] swap-img-to-img (file transfer + progress)")
        _swap_img()
        print("[face2face] add-face + swap with embedding")
        _swap_with_embedding()
        if VIDEO.is_file():
            print("[face2face] swap-video")
            _swap_video()
        else:
            print(f"[face2face] skip video, missing {VIDEO}")
    print("[face2face] PASS")


if __name__ == "__main__":
    run()
