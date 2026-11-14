import csv, os
from pathlib import Path
import pytest
from ml.pose_extractor import extract_pose
from ml.angle_calculator import detect_shooting_side, angles_for_video
from ml.release_frame_detector import find_release_frame

CLIPS = Path(os.environ.get("CLIPS_DIR", "~/clips")).expanduser()
KEY = Path(__file__).resolve().parents[2] / "data" / "release_frames.csv"
MAX_AVG_ERROR = 24.0  # Sixers#02 result (22.0 frames) + 2

@pytest.mark.skipif(not CLIPS.is_dir(), reason="answer-key clips folder not found")
def test_release_accuracy():
    errors = []
    for name, truth, *_ in list(csv.reader(open(KEY)))[1:]:
        path = CLIPS / name
        if not path.exists():
            continue
        frames = extract_pose(str(path))["frames"]
        side = detect_shooting_side(frames)
        elbow = [a["elbow_angle"] for a in angles_for_video(frames)]
        found, _ = find_release_frame(frames, elbow, side)
        if found is not None:
            errors.append(abs(found - int(truth)))
    assert errors, "detector found no release frame on any clip"
    assert sum(errors) / len(errors) <= MAX_AVG_ERROR