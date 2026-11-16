# Free-throw form dataset (data/features.csv)
One row per shot: pose-based form measurements taken at a hand-marked release frame, plus whether the shot was made. Built for Sprint 8's "does good form predict makes?" experiments.


## How it was built
1. **Release frames were marked by hand.** For each clip I opened python ml/tools/frame_viewer.py <clip>, stepped frame by frame, and recorded the first frame where the ball is no longer touching the shooter's fingertips. These are stored in data/release_frames_all.csv (filename,release_frame,made,player). The automatic detector (ml/release_frame_detector.py) was not used, because it was still being fixed.
2. **ml/tools/build_dataset.py** reads that file, runs the pose pipeline (extract_pose) and angle functions (angles_for_video) on each clip, and writes the measurements at and before the marked release frame.
3. Run with: python ml/tools/build_dataset.py ~/clips data/release_frames_all.csv data/features.csv

## Columns
| Column | Meaning |
|---|---|
| `filename` | Clip file name |
| `player` | Name part of the file name |
| `made` | 1 = made, 0 = missed |
| `side` | Shooting side detected by `detect_shooting_side` |
| `release_frame` | Hand-marked frame where the ball leaves the fingertips |
| `fps` | Frames per second of the clip |
| `elbow_at_release` | Elbow angle (degrees) at release |
| `knee_at_release` | Knee angle (degrees) at release |
| `shoulder_at_release` | Shoulder angle (degrees) at release |
| `min_knee_before_release` | Smallest knee angle before release (how deep the dip was) |
| `min_elbow_before_release` | Smallest elbow angle before release (the set point) |
| `dip_to_release_s` | Seconds from the deepest knee bend to release |
| `pose_coverage` | Share of frames where pose landmarks were found |

## Skipped clips:

**The following clips were rendered unusable as they did not have a pose detected by build_dataset.py. This is likely due to the blurriness of many clips, and some shooters may be too small or far from the camera.**

### Made (48)
Abby_made_02.mp4, Abby_made_05.mp4, Anisha_Made_03.mp4, Anisha_Made_04.mp4, Anisha_Made_08.mp4, Audrey_made_01.mp4, Audrey_made_04.mp4, Audrey_made_05.mp4, Audrey_made_06.mp4, Audrey_made_07.mp4, Audrey_made_08.mp4, David_made_01.mp4, David_made_02.mp4, David_made_03.mp4, David_made_04.mp4, David_made_05.mp4, David_made_07.mp4, David_made_08.mp4, Freya_Made_1.mp4, Freya_Made_2.mp4, Freya_Made_5.mp4, Kelvin_Huang_01_Make.mp4, Kelvin_Huang_04_Make.mp4, Kelvin_Huang_06_Make.mp4, Kelvin_Huang_08_Make.mp4, Manoj_Made_03.mp4, Manoj_Made_04.mp4, Manoj_Made_07.mp4, Manoj_Made_08.mp4, Rijul_made_01.mp4, Rijul_made_02.mp4, Rijul_made_03.mp4, Rijul_made_04.mp4, Rijul_made_05.mp4, Rijul_made_07.mp4, Rijul_made_08.mp4, Ryan_made_03.mp4, Ryan_made_04.mp4, Ryan_made_07.mp4, Ryan_made_08.mp4, Ryan_made_09.mp4, Ryan_made_14.mp4, Veronica_made_04.mp4, Veronica_made_06.mp4, Veronica_made_08.mp4, make1.mp4, make4.mp4, make7.mp4

### Missed (48)
Abby_missed_03.mp4, Abby_missed_04.mp4, Abby_missed_06.mp4, Anisha_Missed_01.mp4, Anisha_Missed_03.mp4, Anisha_Missed_05.mp4, Anisha_Missed_07.mp4, Anisha_Missed_08.mp4, Audrey_missed_01.mp4, Audrey_missed_05.mp4, Audrey_missed_06.mp4, Audrey_missed_07.mp4, David_Missed_01.mp4, David_Missed_03.mp4, David_Missed_04.mp4, David_Missed_05.mp4, David_Missed_08.mp4, Freya_Missed_4.mp4, Freya_Missed_6.mp4, Freya_Missed_7.mp4, Freya_Missed_8.mp4, Kelvin_Huang_04_Missed.mp4, Kelvin_Huang_05_Missed.mp4, Kelvin_Huang_06_Missed.mp4, Kelvin_Huang_07_Missed.mp4, Kelvin_Huang_08_Missed.mp4, Kelvin_Huang_09_Missed.mp4, Manoj_Missed_01.mp4, Manoj_Missed_03.mp4, Manoj_Missed_05.mp4, Rijul_missed_01.mp4, Rijul_missed_02.mp4, Rijul_missed_03.mp4, Rijul_missed_04.mp4, Rijul_missed_05.mp4, Rijul_missed_06.mp4, Rijul_missed_08.mp4, Ryan_missed_06.mp4, Ryan_missed_08.mp4, Veronica_missed_05.mp4, Veronica_missed_06.mp4, Veronica_missed_07.mp4, Veronica_missed_08.mp4, miss3.mp4, miss4.mp4, miss5.mp4, miss6.mp4, miss7.mp4
