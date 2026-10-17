
import json
import sys
import tempfile
import time
from datetime import datetime, timezone

from ml.pose_extractor import extract_pose
from ml.angle_calculator import detect_shooting_side, angles_for_video
from ml.release_frame_detector import find_release_frame
from ml.feedback_rules import evaluate_form
from ml.skeleton_overlay import draw_skeleton
from ml.angle_labels import draw_angle_labels
from ml.video_encoder import encode_video
from ml.video_io import iter_frames


ANGLE_KEYS = ("elbow_angle", "knee_angle", "shoulder_angle")


def _pixel_landmarks(landmarks, width, height):
    """Convert normalized pose coordinates to pixel coordinates."""
    if landmarks is None:
        return None

    converted = []
    for landmark in landmarks:
        point = dict(landmark)

        x = point.get("x")
        y = point.get("y")

        point["x"] = int(x * width) if x is not None else None
        point["y"] = int(y * height) if y is not None else None

        converted.append(point)

    return converted


def _json_number(value):
    """Convert NumPy numeric values to ordinary Python numbers."""
    if value is None:
        return None

    number = float(value)
    if not __import__("math").isfinite(number):
        return None

    return number


def analyze(video_path):
    """Analyze a free-throw video and return (result_dict, annotated_video_path)."""
    pose = extract_pose(video_path)
    frames = pose["frames"]

    if not frames:
        raise ValueError("The video contains no frames to analyze.")

    side = detect_shooting_side(frames)
    per_frame = angles_for_video(frames)

    release, reason = find_release_frame(
        frames,
        [item["elbow_angle"] for item in per_frame],
        side,
    )

    # If release detection fails, return the reason as the only feedback item.
    if release is None:
        result = {
            "session_id": None,
            "release_frame": None,
            "angles": {key: None for key in ANGLE_KEYS},
            "feedback": [
                {
                    "checkpoint": "release_detection",
                    "angle": None,
                    "status": "needs_work",
                    "tip": reason,
                }
            ],
            "overall_score": None,
            "annotated_video_url": None,
            "processed_at": datetime.now(timezone.utc).isoformat(),
        }
        return result, None

    # Find the release frame's angle measurements by frame number.
    release_index = next(
        (
            index
            for index, item in enumerate(per_frame)
            if item["frame"] == release
        ),
        None,
    )

    if release_index is None:
        raise ValueError(f"Release frame {release} has no angle measurements.")

    release_angles = per_frame[release_index]
    angles = {key: release_angles.get(key) for key in ANGLE_KEYS}

    form = evaluate_form(angles)
    statuses = {
        item["checkpoint"]: item["status"]
        for item in form["feedback"]
    }

    # Draw annotations on each original video frame.
    annotated_frames = []
    width = pose["width"]
    height = pose["height"]

    for frame_number, frame in iter_frames(video_path):
        if frame_number < len(frames):
            landmarks = _pixel_landmarks(
                frames[frame_number]["landmarks"],
                width,
                height,
            )
            frame_angles = per_frame[frame_number]
        else:
            landmarks = None
            frame_angles = {key: None for key in ANGLE_KEYS}

        frame = draw_skeleton(frame, landmarks, statuses, side)
        frame = draw_angle_labels(frame, landmarks, frame_angles, side)
        annotated_frames.append(frame)

    if not annotated_frames:
        raise ValueError("No video frames were available for encoding.")

    # Create a temporary output MP4.
    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmp:
        out_path = tmp.name

    encode_video(annotated_frames, pose["fps"], out_path)

    result = {
        "session_id": None,
        "release_frame": int(release),
        "angles": {
            key: _json_number(value)
            for key, value in angles.items()
        },
        "feedback": form["feedback"],
        "overall_score": (
            int(form["overall_score"])
            if form["overall_score"] is not None
            else None
        ),
        "annotated_video_url": None,
        "processed_at": datetime.now(timezone.utc).isoformat(),
    }

    return result, out_path


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(
            "Usage: python -m ml.analysis_pipeline path/to/clip.mp4",
            file=sys.stderr,
        )
        sys.exit(2)

    start = time.perf_counter()

    try:
        result, output_path = analyze(sys.argv[1])
        print(json.dumps(result, indent=2, allow_nan=False))
        print(f"Annotated video: {output_path}")
    except Exception as exc:
        print(f"Analysis failed: {exc}", file=sys.stderr)
        sys.exit(1)
    finally:
        print(f"Runtime: {time.perf_counter() - start:.2f} seconds")
