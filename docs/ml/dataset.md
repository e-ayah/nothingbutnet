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

## Status: 21 of 185 labeled clips currently in features.csv
- 33 of the 185 labeled clips have video files available locally so far.
- Of those 33, 21 produced usable features; 12 were skipped for having no
  detectable pose/elbow angle right at the labeled release frame (listed in
  `build_dataset.py`'s output; every one of these 12 also appears in
  Veronica's own skipped-clip list, which is a good consistency check).
- The remaining 152 labeled clips (covering Audrey, David, Freya,
  Kelvin_Huang, Manoj, most of Rijul/Ryan/Veronica's made shots, and the
  generic make/miss clips) still need their video files downloaded before
  `build_dataset.py` can process them.

## What's left
- Track down the full clips folder (Veronica likely still has it locally,
  or it's in the team Drive) and download the remaining 152 clips so the
  full dataset can be processed.
- Re-run `python -m ml.tools.build_dataset.py ~/clips data/release_frames_all.csv data/features.csv`
  once those are downloaded.
- Note for the team: Finals#10 (Experiments B) and #11 (Experiments C)
  both ran against an earlier, much smaller features.csv (8 rows) and
  Experiments C explicitly flagged C1 as blocked by insufficient data -
  worth re-running those once the fuller dataset lands, even though it's
  past the original deadline.
