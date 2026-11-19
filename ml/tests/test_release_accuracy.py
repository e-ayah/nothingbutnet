"""Release-frame accuracy (Finals#04).

Fast unit tests for the "refuse instead of guessing" checks, plus slow tests
on the answer-key clips that skip when the clips aren't downloaded
(CLIPS_DIR, default ~/clips).

Clean-set number this guards (Finals#04, testing/reports/accuracy.md):
shooter-only 480 px clips (Mac, M3 Pro) -> 6/11 within ±3 frames; 8/11 get a
release (average error 3.4 frames on those), the other 3 are refused with a reason.
"""
import csv
import os
import subprocess
import tempfile
from pathlib import Path

import pytest

from ml.release_frame_detector import (
    REASON_ROTATED, REASON_SPLICED, find_release_frame, looks_rotated,
    looks_spliced, missing_near)

CLIPS = Path(os.environ.get("CLIPS_DIR", "~/clips")).expanduser()
KEY = Path(__file__).resolve().parents[2] / "data" / "release_frames.csv"

# Clean answer-key clips (Quality = clean in testing/test-videos.md) and the
# shooter's horizontal position (fraction of frame width) during the shot.
# Broadcast footage has several players; MediaPipe tracks one person, often
# the wrong one, so the accuracy test crops to the shooter - the same "only
# the shooter in frame" footage the app asks users to film.
SHOOTER_X = {
    "Kelvin_Huang_05_Missed.mp4": 0.33, "Veronica_made_03.mp4": 0.17,
    "Veronica_made_01.mp4": 0.30, "Veronica_missed_03.mp4": 0.68,
    "Kelvin_Huang_08_Missed.mp4": 0.29, "Manoj_Missed_07.mp4": 0.09,
    "Freya_Made_7.mp4": 0.65, "Kelvin_Huang_04_Make.mp4": 0.30,
    "Kelvin_Huang_06_Make.mp4": 0.24, "Kelvin_Huang_09_Make.mp4": 0.25,
    "Veronica_made_04.mp4": 0.69,
}
FINAL_WITHIN_3 = 6      # of 11
FINAL_AVG_ERROR = 3.4   # frames, over detected clips
FINAL_REFUSED = 3       # clean clips returned as None
WITHIN_3_SLACK = 2      # MediaPipe output differs a little between machines
AVG_SLACK = 5.0


# ---------- fast unit tests (no videos) ----------

def body(frame, cx=500.0, cy=500.0, torso=200.0, sideways=False):
    """33 landmarks with a realistic torso centred at (cx, cy)."""
    lm = [{"x": cx + i, "y": cy + i, "visibility": 1.0} for i in range(33)]
    h = torso / 2
    if sideways:  # shoulders left of hips, like a 90° rotated video
        sh, hp = [(cx - h, cy - 20), (cx - h, cy + 20)], [(cx + h, cy - 15), (cx + h, cy + 15)]
    else:
        sh, hp = [(cx - 20, cy - h), (cx + 20, cy - h)], [(cx - 15, cy + h), (cx + 15, cy + h)]
    for idx, (x, y) in zip((11, 12, 23, 24), sh + hp):
        lm[idx] = {"x": x, "y": y, "visibility": 1.0}
    return {"frame": frame, "landmarks": lm}


def test_missing_near_counts_longest_gap():
    frames = [body(i) for i in range(30)]
    for i in range(12, 19):
        frames[i]["landmarks"] = None
    assert missing_near(frames, 15) == 7
    assert missing_near(frames, 2) == 0


def test_steady_body_is_not_spliced():
    frames = [body(i, cx=400 + i * 3) for i in range(60)]
    assert not looks_spliced(frames)


def test_one_frame_glitch_is_not_spliced():
    frames = [body(i) for i in range(60)]
    frames[30] = body(30, cx=1500)  # pose jumps to someone else for one frame, then back
    assert not looks_spliced(frames)


def test_cut_to_another_person_is_spliced():
    frames = [body(i, cx=300, torso=120) for i in range(20)]
    frames += [body(i, cx=1200, torso=260) for i in range(20, 60)]
    assert looks_spliced(frames)
    found, reason = find_release_frame(frames, [170.0] * 60, "right")
    assert found is None and reason == REASON_SPLICED


def test_sideways_video_is_rejected():
    frames = [body(i, sideways=True) for i in range(40)]
    assert looks_rotated(frames)
    assert not looks_rotated([body(i) for i in range(40)])
    found, reason = find_release_frame(frames, [170.0] * 40, "right")
    assert found is None and reason == REASON_ROTATED


# ---------- slow tests on the answer-key clips ----------

def _labels():
    with open(KEY, newline="") as f:
        return {r["filename"]: int(r["release_frame"]) for r in csv.DictReader(f)}


def _detect(path):
    from ml.pose_extractor import extract_pose
    from ml.angle_calculator import detect_shooting_side, angles_for_video
    frames = extract_pose(str(path))["frames"]
    elbow = [a["elbow_angle"] for a in angles_for_video(frames)]
    return find_release_frame(frames, elbow, detect_shooting_side(frames))


def _shooter_480(src, x, out_dir):
    """Crop to 30% of the width around the shooter, then scale to 480 px wide
    (what the server analyzes). Every frame is kept so numbers match the key."""
    import cv2
    import imageio_ffmpeg
    cap = cv2.VideoCapture(str(src))
    w, h = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    cap.release()
    cw = int(w * 0.30) // 2 * 2
    x0 = max(0, min(w - cw, int(x * w - cw / 2)))
    dst = Path(out_dir) / src.name
    subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), "-y", "-loglevel", "error", "-i", str(src),
                    "-vf", f"crop={cw}:{h}:{x0}:0,scale=480:-2", "-fps_mode", "passthrough",
                    "-an", str(dst)], check=True)
    return dst


@pytest.mark.skipif(not CLIPS.is_dir(), reason="answer-key clips folder not found")
def test_clean_set_release_accuracy():
    labels, errors = _labels(), []
    with tempfile.TemporaryDirectory() as tmp:
        for name, x in SHOOTER_X.items():
            src = CLIPS / name
            if not src.exists():
                pytest.skip(f"missing clip {name}")
            found, _ = _detect(_shooter_480(src, x, tmp))
            errors.append(None if found is None else abs(found - labels[name]))
    detected = [e for e in errors if e is not None]
    assert sum(e <= 3 for e in detected) >= FINAL_WITHIN_3 - WITHIN_3_SLACK, errors
    assert sum(detected) / len(detected) <= FINAL_AVG_ERROR + AVG_SLACK, errors
    assert len(errors) - len(detected) <= FINAL_REFUSED + WITHIN_3_SLACK, errors


@pytest.mark.skipif(not CLIPS.is_dir(), reason="answer-key clips folder not found")
@pytest.mark.parametrize("name", ["Anisha_Made_05.mp4", "Rijul_missed_05.mp4"])
def test_sideways_bad_clips_fail_gracefully(name):
    if not (CLIPS / name).exists():
        pytest.skip(f"missing clip {name}")
    found, reason = _detect(CLIPS / name)
    assert found is None and reason == REASON_ROTATED
