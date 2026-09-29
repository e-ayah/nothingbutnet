import pytest

from ml.video_io import video_info, read_frames

VIDEO_PATH = "ml/tests/data/tiny.mp4"

def test_video_info():
    info = video_info(VIDEO_PATH)

    assert info["fps"] > 0
    assert info["width"] == 480
    assert info["height"] > 0
    assert info["frame_count"] > 0
    assert info["duration_s"] > 0

def test_read_frames():
    info = video_info(VIDEO_PATH)
    frames = read_frames(VIDEO_PATH)

    assert len(frames) == info["frame_count"]

def test_missing_file():
    with pytest.raises(ValueError):
        video_info("ml/tests/data/does_not_exist.mp4")