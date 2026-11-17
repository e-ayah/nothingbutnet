# Finals #09 — Made/Missed Dataset (Part 1)

## How frames were marked
Each clip was stepped through frame by frame with `ml/tools/frame_viewer.py`,
which overlays the frame index on the video. The release frame is the first
frame where the ball visibly leaves the shooter's fingertips. `made`/`player`
are parsed from each filename (e.g. `Veronica_made_05.mp4` -> player
`Veronica`, made `1`).

`data/release_frames_all.csv` (185 clips) is Veronica Ting's labeling work
from an earlier, unmerged `ml/sixers-dataset` branch (Sixers#09, which never
got an owner at the time), picked up and finished here since it is far more
complete than the ~20 clips originally labeled for this ticket. Where it
overlaps with our own labels, the release frames matched within 1-3 frames
in every case but one.

One labeling inconsistency was found and fixed while finishing this: Kelvin
Huang's made clips were labeled with player `Kelvin_Huang` but his missed
clips were labeled `Kelvin` — same person, inconsistent name. Left as-is,
this would have looked like two separate, fully-confounded players (one
all-makes, one all-misses). Normalized to `Kelvin_Huang` for all 19 of his
clips.

## Columns in features.csv
- `filename`, `player`, `made` (1/0), `side`, `release_frame`, `fps`
- `elbow_at_release`, `knee_at_release`, `shoulder_at_release`
- `min_knee_before_release`, `min_elbow_before_release`, `dip_to_release_s`
- `arm_visibility_at_release`: average MediaPipe landmark visibility of the
  shooting shoulder, elbow and wrist at the release frame
- `pose_coverage`: share of frames in the clip where MediaPipe found a pose

`arm_visibility_at_release` was added in this ticket's `build_dataset.py` -
Veronica's original script did not compute it, and Finals#10/#11 rely on
this exact column name.

## Status: complete — 89 of 185 labeled clips in features.csv
- All 185 labeled clips now have video files available locally.
- Of those 185, 89 produced usable features; 96 were skipped for having no
  detectable pose/elbow angle right at the labeled release frame (listed in
  `build_dataset.py`'s output). This skip count is almost an exact match for
  Veronica's own independently-reported skip count from her original
  branch, which is a good consistency check on the pipeline.
- Every one of the 11 players represented has a mix of made and missed
  shots, so player and outcome are no longer confounded the way they were
  in the earlier partial (21-row) version of this dataset.

## What's left
- Finals#10 (Experiments B) and #11 (Experiments C) both ran against an
  earlier, much smaller features.csv (8 rows) and Experiments C explicitly
  flagged C1 as blocked by insufficient data - worth re-running those now
  that the full 89-row dataset is available, even though it's past the
  original deadline.
- The 96 skipped clips are a real data loss, not just a formatting
  problem - if a future ticket wants to shrink that number, it would need
  to look at why MediaPipe fails to find a pose at those specific release
  frames (camera angle, occlusion, etc.), not just re-run the same pipeline.
