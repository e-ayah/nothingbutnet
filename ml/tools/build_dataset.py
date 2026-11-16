import csv
import sys
from pathlib import Path
 
# Make `from ml...` work when this file is run as a script from the repo root.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
 
from ml.pose_extractor import extract_pose
from ml.angle_calculator import detect_shooting_side, angles_for_video
 
FIELDS = [
    "filename", "player", "made", "side", "release_frame", "fps",
    "elbow_at_release", "knee_at_release", "shoulder_at_release",
    "min_knee_before_release", "min_elbow_before_release",
    "dip_to_release_s", "pose_coverage",
]
 
 
def build_row(clip_path, r):
    """Return (row, None) on success or (None, reason) if the clip must be skipped."""
    rel_text = (r.get("release_frame") or "").strip()
    if not rel_text:
        return None, "no release frame marked"
    try:
        rel = int(rel_text)
    except ValueError:
        return None, f"release_frame is not a number: {rel_text!r}"
 
    if not clip_path.exists():
        return None, f"file not found: {clip_path}"
 
    pose = extract_pose(str(clip_path))
    frames, fps = pose["frames"], pose["fps"] or 30
    if not frames:
        return None, "no frames could be read from the video"
 
    per = angles_for_video(frames)
    if rel < 0 or rel >= len(per):
        return None, f"release frame {rel} is outside the video ({len(per)} frames)"
    if per[rel]["elbow_angle"] is None:
        return None, "pose missing at release frame"
 
    before = per[: rel + 1]
    knees = [(a["knee_angle"], i) for i, a in enumerate(before)
             if a["knee_angle"] is not None]
    elbows = [a["elbow_angle"] for a in before if a["elbow_angle"] is not None]
    min_knee, dip_frame = min(knees) if knees else (None, None)
 
    with_landmarks = sum(f["landmarks"] is not None for f in frames)
    row = {
        "filename": r["filename"],
        "player": r["player"],
        "made": r["made"],
        "side": detect_shooting_side(frames),
        "release_frame": rel,
        "fps": fps,
        "elbow_at_release": per[rel]["elbow_angle"],
        "knee_at_release": per[rel]["knee_angle"],
        "shoulder_at_release": per[rel]["shoulder_angle"],
        "min_knee_before_release": min_knee,
        "min_elbow_before_release": min(elbows) if elbows else None,
        "dip_to_release_s": None if dip_frame is None else round((rel - dip_frame) / fps, 3),
        "pose_coverage": round(with_landmarks / len(frames), 3),
    }
    return row, None
 
 
def main():
    if len(sys.argv) != 4:
        sys.exit("usage: python ml/tools/build_dataset.py CLIPS_DIR KEY_CSV OUT_CSV")
    clips_dir = Path(sys.argv[1]).expanduser()
    key_path, out_path = sys.argv[2], sys.argv[3]
 
    rows, skipped = [], []
    with open(key_path, newline="") as f:
        key_rows = list(csv.DictReader(f))
 
    for n, r in enumerate(key_rows, 1):
        name = r["filename"]
        folder = "made" if str(r["made"]).strip() == "1" else "missed"
        print(f"[{n}/{len(key_rows)}] {name}")
        try:
            row, reason = build_row(clips_dir / folder / name, r)
        except Exception as e:  # a crashing clip is skipped, not fatal
            row, reason = None, f"error: {type(e).__name__}: {e}"
        if row is None:
            skipped.append((name, reason))
        else:
            rows.append(row)
 
    if not rows:
        print("No usable rows, so nothing was written.")
    else:
        with open(out_path, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=FIELDS)
            w.writeheader()
            w.writerows(rows)
 
    made = sum(str(r["made"]).strip() == "1" for r in rows)
    print(f"\nwrote {len(rows)} rows ({made} made, {len(rows) - made} missed) "
          f"· skipped {len(skipped)}")
    for name, reason in skipped:
        print(f"  skipped {name}: {reason}")
 
 
if __name__ == "__main__":
    main()
 