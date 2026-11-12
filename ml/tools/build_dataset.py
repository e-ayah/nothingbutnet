import csv, sys
from pathlib import Path
from ml.pose_extractor import extract_pose
from ml.angle_calculator import detect_shooting_side, angles_for_video

ARM = {"right": (12, 14, 16), "left": (11, 13, 15)}

def arm_visibility(frame, side):
    lm = frame["landmarks"]
    if not lm:
        return None
    return round(sum(lm[i]["visibility"] for i in ARM[side]) / 3, 3)

clips_dir, key_path, out_path = Path(sys.argv[1]).expanduser(), sys.argv[2], sys.argv[3]
rows, skipped = [], []
for r in csv.DictReader(open(key_path)):
    folder = "made" if r["made"] == "1" else "missed"
    pose = extract_pose(str(clips_dir / folder / r["filename"]))
    frames, fps = pose["frames"], pose["fps"] or 30
    rel = int(r["release_frame"])
    per = angles_for_video(frames)
    if rel >= len(per) or per[rel]["elbow_angle"] is None:
        skipped.append(r["filename"])
        continue
    before = per[:rel + 1]
    knees = [(a["knee_angle"], a["frame"]) for a in before if a["knee_angle"] is not None]
    elbows = [a["elbow_angle"] for a in before if a["elbow_angle"] is not None]
    min_knee, dip_frame = min(knees) if knees else (None, None)
    side = detect_shooting_side(frames)
    rows.append({
        "filename": r["filename"], "player": r["player"], "made": r["made"],
        "side": side, "release_frame": rel, "fps": fps,
        "elbow_at_release": per[rel]["elbow_angle"], "knee_at_release": per[rel]["knee_angle"],
        "shoulder_at_release": per[rel]["shoulder_angle"],
        "min_knee_before_release": min_knee, "min_elbow_before_release": min(elbows) if elbows else None,
        "dip_to_release_s": None if dip_frame is None else round((rel - dip_frame) / fps, 3),
        "pose_coverage": round(sum(f["landmarks"] is not None for f in frames) / len(frames), 3),
        "arm_visibility_at_release": arm_visibility(frames[rel], side),
    })

with open(out_path, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]))
    w.writeheader()
    w.writerows(rows)
print(f"wrote {len(rows)} rows, skipped {len(skipped)}: {skipped}")

