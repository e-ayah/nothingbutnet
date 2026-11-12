# Finals #09 — Made/Missed Dataset (Part 1)

## How frames were marked
Each clip was stepped through frame by frame with `ml/tools/frame_viewer.py`,
which overlays the frame index on the video. The release frame is the first
frame where the ball visibly leaves the shooter's fingertips. `made`/`player`
are parsed from each filename (e.g. `Veronica_made_05.mp4` -> player
`Veronica`, made `1`).

## Columns in features.csv
- `filename`, `player`, `made` (1/0), `side`, `release_frame`, `fps`
- `elbow_at_release`, `knee_at_release`, `shoulder_at_release`
- `min_knee_before_release`, `min_elbow_before_release`, `dip_to_release_s`
- `arm_visibility_at_release`: average MediaPipe landmark visibility of the
  shooting shoulder, elbow and wrist at the release frame
- `pose_coverage`: share of frames in the clip where MediaPipe found a pose

## Made/missed counts per player (release_frames_all.csv, 20 clips labeled so far)
- Veronica: 3 made, 4 missed
- Anisha: 3 made, 0 missed
- Abby: 3 made, 0 missed
- Rijul: 1 made, 1 missed
- Kelvin_Huang: 0 made, 2 missed
- Manoj: 0 made, 1 missed
- Ryan: 0 made, 2 missed

## Skipped clips
- `Abby_made_02.mp4`, `Rijul_made_03.mp4`: no clean elbow angle detected at
  the labeled release frame (pose lost or occluded), so `build_dataset.py`
  skipped them rather than guess.

## What's left
- 10 of the 20 labeled clips (the original answer-key set) still need their
  video files downloaded individually from the Drive links in
  `testing/test-videos.md` before they can be run through `build_dataset.py`.
- Roughly 19 more downloaded clips in `~/clips/made` and `~/clips/missed`
  still need release frames hand-marked.
- `features.csv` currently has 8 rows; it will grow as the above gets
  finished before Sunday's deadline.
  