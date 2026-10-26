
import csv
import sys
from pathlib import Path

from ml.pose_extractor import extract_pose
from ml.angle_calculator import detect_shooting_side, angles_for_video
from ml.release_frame_detector import find_release_frame


def main():
    if len(sys.argv) != 3:
        print(
            "Usage: python ml/tools/eval_release.py "
            "CLIPS_DIR ANSWER_KEY.csv"
        )
        return

    clips_dir = Path(sys.argv[1]).expanduser()
    key_path = Path(sys.argv[2])

    rows = []

    with open(key_path, newline="") as csv_file:
        reader = csv.DictReader(csv_file)

        for r in reader:
            video_path = clips_dir / r["filename"]

            if not video_path.exists():
                print("Missing video:", video_path)
                continue

            pose = extract_pose(str(video_path))
            frames = pose["frames"]

            side = detect_shooting_side(frames)
            per_frame = angles_for_video(frames)

            elbow_angles = [
                a["elbow_angle"] for a in per_frame
            ]

            found, reason = find_release_frame(
                frames, elbow_angles, side
            )

            truth = int(r["release_frame"])
            error = None if found is None else abs(found - truth)

            # Match angles by frame number rather than assuming
            # the frame number is the list index.
            angle_by_frame = {
                a["frame"]: a for a in per_frame
            }
            angles = angle_by_frame.get(found, {}) if found is not None else {}

            rows.append({
                "filename": r["filename"],
                "truth": truth,
                "found": found,
                "error": error,
                "side": side,
                "elbow": angles.get("elbow_angle"),
                "knee": angles.get("knee_angle"),
                "shoulder": angles.get("shoulder_angle"),
                "reason": reason or ""
            })

    print(
        "| Clip | Answer key | Detected | Error (frames) "
        "| Side | Elbow | Knee | Shoulder | Note |"
    )
    print(
        "|---|---:|---:|---:|---|---:|---:|---:|---|"
    )

    def fmt(value):
        return "—" if value is None else f"{value:.1f}"

    for r in rows:
        detected = (
            r["found"] if r["found"] is not None else "Missed"
        )
        error = (
            r["error"] if r["error"] is not None else "Missed"
        )

        print(
            f'| {r["filename"]} | {r["truth"]} '
            f'| {detected} | {error} | {r["side"]} '
            f'| {fmt(r["elbow"])} | {fmt(r["knee"])} '
            f'| {fmt(r["shoulder"])} | {r["reason"]} |'
        )

    errors = [
        r["error"] for r in rows
        if r["error"] is not None
    ]
    missed = sum(
        r["found"] is None for r in rows
    )

    if errors:
        print(
            f"\nAverage error among detected clips: "
            f"{sum(errors) / len(errors):.1f} frames"
        )
        print(
            f"Within ±2 frames: "
            f"{sum(e <= 2 for e in errors)}/{len(rows) - missed} "
            f"detected clips"
        )
    else:
        print("\nNo clips had a detected release frame.")

    print(f"Missed clips: {missed}/{len(rows)}")


if __name__ == "__main__":
    main()
