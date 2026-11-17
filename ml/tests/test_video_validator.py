from pathlib import Path

import cv2
import numpy as np
import pytest

from ml.video_validator import validate


POSE_CLIP = Path(__file__).parent / "data" / "pose_clip.mp4"


def make_video(path: Path, *, seconds: int = 2, brightness: int = 128) -> None:
    """Generate a small MP4 with a uniform brightness and no person."""
    width, height = 160, 120
    fps = 10
    writer = cv2.VideoWriter(
        str(path), cv2.VideoWriter_fourcc(*"mp4v"), fps, (width, height)
    )
    frame = np.full((height, width, 3), brightness, dtype=np.uint8)

    try:
        assert writer.isOpened(), f"Could not create test video {path.name}"
        for _ in range(seconds * fps):
            writer.write(frame)
    finally:
        writer.release()


def test_rejects_video_over_fifteen_seconds(tmp_path):
    path = tmp_path / "long.mp4"
    make_video(path, seconds=16)

    ok, reason = validate(str(path))

    assert ok is False
    assert reason is not None and "too long" in reason


@pytest.mark.parametrize("seconds", [2, 15])
def test_rejects_dark_video_at_or_below_duration_limit(tmp_path, seconds):
    path = tmp_path / "dark.mp4"
    make_video(path, seconds=seconds, brightness=5)

    ok, reason = validate(str(path))

    assert ok is False
    assert reason is not None and "too dark" in reason


def test_rejects_video_without_a_person(tmp_path):
    path = tmp_path / "no_person.mp4"
    make_video(path)

    ok, reason = validate(str(path))

    assert ok is False
    assert reason is not None and "find a person" in reason


def test_accepts_video_with_a_pose():
    assert validate(str(POSE_CLIP)) == (True, None)


def test_rejects_unreadable_video(tmp_path):
    path = tmp_path / "invalid.mp4"
    path.write_text("This file contains no video.", encoding="utf-8")

    ok, reason = validate(str(path))

    assert ok is False
    assert reason is not None and "couldn't read" in reason