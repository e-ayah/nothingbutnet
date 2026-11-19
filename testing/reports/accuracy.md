# Accuracy Report: Release Frame + Angles (Valkyries#07)

Compares the detected release frame with the hand-marked answer key (`data/release_frames.csv`) on the 10 test clips in `testing/test-videos.md`.

To rerun: download the clips into one folder, then from the repo root run `python -m ml.tools.eval_release <clips folder> data/release_frames.csv`.

## Summary

- **Average absolute frame error:** 22.7 frames across 9 detected clips
- **Within ±2 frames:** 2/10 clips
- **Missed detections:** 1/10 clips

## Three Worst Clips

### 1. Kelvin_Huang_05_Missed.mp4
- **Frame error:** 55 frames (ground truth: 63, detected: 118)
- **Observation:** The detected frame was well after the actual release. By frame 118, the ball had traveled closer to the net and had been out of the player's fingertips for some time. The video may appear a bit blurry though.
- **Possible explanation:** The ball may have blended into the background after release, making it harder for the detector to identify the correct release timing.

### 2. Veronica_made_05.mp4
- **Frame error:** 40 frames (ground truth: 84, detected: 44)
- **Observation:** The detected frame occurred before the actual release, immediately after the video transitioned from an intro clip featuring a different person to the actual side-view footage. 
- **Possible explanation:** The transition between clips may have affected pose extraction or release-frame detection, causing the detector to select a frame from the beginning of the actual shooting footage rather than the release.

### 3. Kelvin_Huang_08_Missed.mp4
- **Frame error:** 27 frames (ground truth: 96, detected: 69)
- **Observation:** The detected frame occurred while the player was raising the ball near his head in preparation for the shot, before the actual release. No obvious camera-angle or shooting-pose issues were observed.
- **Possible explanation:** The detector may have mistaken the ball-raising phase of the shooting motion for the release. This suggests that the detector may need to better distinguish between preparation and actual ball release.

## Angle Spot-Check

### Kelvin_Huang_05_Missed.mp4
- **Elbow (138.9°):** The player's elbow appeared more extended than the measured angle suggested.
- **Shoulder (144.2°):** The shoulder angle appeared consistent with the player's pose.

### Veronica_made_05.mp4
- **Elbow (1.7°):** The measured elbow angle was significantly different from the player's visible arm position, suggesting a possible angle estimation error.
- **Knee and shoulder:** Angles were unavailable in the evaluation output, so they could not be checked.

### Kelvin_Huang_08_Missed.mp4
- **Elbow (174.5°):** The measured angle appeared reasonably consistent with the player's elbow position.
- **Shoulder (175.7°):** The player's shoulder appeared less extended than the measured angle suggested.
- **Knee:** The angle was unavailable in the evaluation output, so it could not be checked.

## Sixers#02 — Release-frame accuracy

**Changes** (`ml/release_frame_detector.py`)
- Fix 1: fill short landmark gaps (≤ 5 frames) in elbow angle, wrist y and shoulder y with linear interpolation instead of skipping frames. Alone: no change (22.7 → 22.7) — most gaps at the release are 20–70 frames, too long to fill.
- Fix 2: new release rule — first frame where the elbow is ≥ 160° for 2 consecutive frames; falls back to the old rule (first frame within 10° of max elbow) if none. Also tried "wrist at highest point": worse (31.6 frames).

**Results (full-size clips, 10 answer-key clips)**

| Clip | Answer key | Before | After | Error before | Error after |
|---|---:|---:|---:|---:|---:|
| Veronica_made_05 | 84 | 44 | 44 | 40 | 40 |
| Kelvin_Huang_05_Missed | 63 | 118 | 118 | 55 | 55 |
| Veronica_made_03 | 183 | 185 | 185 | 2 | 2 |
| Veronica_made_01 | 56 | Missed | Missed | — | — |
| Veronica_missed_03 | 83 | 96 | 96 | 13 | 13 |
| Kelvin_Huang_08_Missed | 96 | 69 | 72 | 27 | 24 |
| Anisha_Made_05 | 77 | 106 | 104 | 29 | 27 |
| Rijul_missed_05 | 71 | 90 | 90 | 19 | 19 |
| Veronica_missed_04 | 31 | 14 | 14 | 17 | 17 |
| Manoj_Missed_07 | 115 | 117 | 116 | 2 | 1 |
| **Average (detected)** | | | | **22.7** | **22.0** |
| **Within ±3** | | | | **2/10** | **2/10** |

**Target (±3 on 8/10) not met. Clips that still fail and why**
- Kelvin_Huang_05, Rijul_missed_05: no landmarks for 50–100 frames around the release — nothing to detect.
- Veronica_made_05, Kelvin_Huang_08, Veronica_missed_04: detector lands on a one-frame glitch (elbow jumps ~0° → 170°) right before a long gap.
- Anisha_Made_05, Veronica_missed_03: elbow already near full extension before the release, so extension alone can't pinpoint it.
- Veronica_made_01: "wrist never above the shoulder" — possibly wrong shooting side.

**Tests:** updated 3 asserts in `ml/tests/test_release_frame.py` (14 → 13). They encoded the old skip-missing-frames behavior, which this ticket replaces with gap filling.

**Not done yet:** 480 px measurements; Part 2 (ranges from 20+ made shots at hand-marked release frames) — ANGLE_RANGES unchanged.

### Sixers#02 Part 2: feedback ranges

Measured elbow, knee and shoulder at **hand-marked** release frames (`ml/tools/frame_viewer.py`, first frame the ball leaves the hand) on **20 made shots**: Veronica_made_01/03/04/05/07/08, Anisha_Made_01–06, Manoj_Made_01/06, Freya_Made_1/3/4/5/7/8. Range = 10th–90th percentile, rounded to 5°.

| Angle | Old range | New range | Shots with a measured angle |
|---|---|---|---:|
| Elbow | 85–100 | **115–165** | 14 |
| Knee | 150–175 | **140–170** | 15 |
| Shoulder | 45–75 | **10–150** | 16 |

Updated in `ml/feedback_rules.py` (ANGLE_RANGES) and `frontend/constants/ranges.ts` (same numbers).

**Caveats**
- Fewer than 20 values per angle: some joints weren't visible at the release frame.
- Shoulder range (10–150) is very wide — likely bad shoulder/hip landmarks on some clips. Worth a follow-up.
- Anisha_Made_06 (frame 8) and Freya_Made_5 (frame 3) were marked very early in the clip — worth a second look.

**Tests updated for the new ranges:** `test_feedback_rules.py` (elbow values), plus `test_comparator.py` (1 test) and `test_trends.py` (elbow values +65) — these two aren't on the ticket's file list but hard-coded the old 85–100 elbow range.

## Finals#04: clean answer key, honest accuracy

**Clean answer key.** I picked 11 clips on footage quality alone, before running the detector: whole body and ball in frame, filmed from the side, sharp at the release, one continuous take, not rotated. Six come from the old key and five are new (Freya_Made_7, Kelvin_Huang_04/06/09_Make, Veronica_made_04). The new five are hand-labeled with the same rule as the old ones: the first frame where there's a visible gap between the ball and the fingertips. I spot-checked the six existing labels for clean clips and they follow the same rule. The 4 bad clips are flagged in `testing/test-videos.md` and stay in the CSV. Two more were picked from the Drive and then dropped: Freya_Made_8 is the same free throw as Freya_Made_7, and Freya_Made_6, Kelvin_Huang_01/05_Make and Veronica_made_02/06/07/08 have spliced intros. All the David_* and Anisha_* clips are rotated 90°.

**Measured on:** Linux, MediaPipe 0.10.21, `-fps_mode passthrough` so frame numbers match the key. 480 px means 480 wide. **MediaPipe output differs a little between machines.** For example, Kelvin_Huang_05 was "118" on the Sixers#02 Mac run and is "None" here, so re-run on your machine before quoting single clips.

### Per clip, as filmed (full broadcast frame)
"Before" is the Sixers#02 detector and "after" is Finals#04 Path A. Each cell is the detected frame, with the error in brackets.

| Clip | Quality | Hand label | Before full | Before 480 | After full | After 480 | Why None (after, full size) |
|---|---|---:|---|---|---|---|---|
| Veronica_made_05 | bad | 84 | 47 (37) | 124 (40) | None | None | Pose lost near the release |
| Kelvin_Huang_05_Missed | clean | 63 | None | None | None | None | Wrist never goes above the shoulder |
| Veronica_made_03 | clean | 183 | 185 (2) | None | 185 (2) | None |  |
| Veronica_made_01 | clean | 56 | None | 0 (56) | None | 0 (56) | Wrist never goes above the shoulder |
| Veronica_missed_03 | clean | 83 | 96 (13) | 149 (66) | None | None | Tracked person jumps / changes |
| Kelvin_Huang_08_Missed | clean | 96 | 98 (2) | 54 (42) | 98 (2) | None |  |
| Anisha_Made_05 | bad | 77 | 103 (26) | 103 (26) | None | None | Video looks sideways |
| Rijul_missed_05 | bad | 71 | 97 (26) | None | None | None | Video looks sideways |
| Veronica_missed_04 | bad | 31 | 16 (15) | 0 (31) | 16 (15) | 0 (31) |  |
| Manoj_Missed_07 | clean | 115 | None | 117 (2) | None | None | Wrist never goes above the shoulder |
| Freya_Made_7 | clean | 24 | 121 (97) | 129 (105) | 121 (97) | 129 (105) |  |
| Kelvin_Huang_04_Make | clean | 91 | None | 217 (126) | None | 217 (126) | Wrist never goes above the shoulder |
| Kelvin_Huang_06_Make | clean | 182 | None | 8 (174) | None | None | Wrist never goes above the shoulder |
| Kelvin_Huang_09_Make | clean | 126 | 44 (82) | 186 (60) | None | None | Pose lost near the release |
| Veronica_made_04 | clean | 59 | 171 (112) | 178 (119) | None | 178 (119) | Tracked person jumps / changes |

| Set (full broadcast frame) | Size | Within ±3 | Release found | Avg error (found only) |
|---|---|---|---|---|
| Clean, before | full / 480 | 2/11 / 1/11 | 6 / 9 | 51.3 / 83.3 |
| Clean, after | full / 480 | 2/11 / 0/11 | 3 / 4 | 33.7 / 101.5 |
| Bad, before | full / 480 | 0/4 / 0/4 | 4 / 3 | 26.0 / 32.3 |
| Bad, after | full / 480 | 0/4 / 0/4 | 1 / 1 | 15.0 / 31.0 |
| All 15, before | full / 480 | 2/15 / 1/15 | 10 / 12 | 41.2 / 70.6 |

**Why clean clips still fail: the pose is on the wrong player.** In broadcast footage there are 8 to 10 people on screen, and MediaPipe Pose tracks one of them, often not the shooter. I checked the 15 frames before each hand label to see whether the tracked body was the shooter. It was for only 3 runs, which were Veronica_made_03 (full size), Kelvin_08 (full size) and Manoj_07 (480). All 3 were **2 frames off**, and every other run was on another player or had no pose. So the "Wrist never goes above the shoulder" results are mostly a bystander standing still. See `docs/writeups/img/wrong_person_Veronica_made_01.jpg`.

### Clean clips with only the shooter in frame (what the app asks users to film)
Same 11 clips, cropped to 30% of the width around the shooter and scaled to 480 px. `ml/tests/test_release_accuracy.py` builds exactly this.

| Clip | Hand label | Rule only | With Path A checks | Why None |
|---|---:|---|---|---|
| Kelvin_Huang_05_Missed | 63 | 73 (10) | None | Tracked person jumps / changes |
| Veronica_made_03 | 183 | 185 (2) | 185 (2) |  |
| Veronica_made_01 | 56 | None | None | Wrist never goes above the shoulder |
| Veronica_missed_03 | 83 | None | None | Wrist never goes above the shoulder |
| Kelvin_Huang_08_Missed | 96 | 98 (2) | 98 (2) |  |
| Manoj_Missed_07 | 115 | None | None | Wrist never goes above the shoulder |
| Freya_Made_7 | 24 | 26 (2) | 26 (2) |  |
| Kelvin_Huang_04_Make | 91 | 92 (1) | 92 (1) |  |
| Kelvin_Huang_06_Make | 182 | 185 (3) | 185 (3) |  |
| Kelvin_Huang_09_Make | 126 | None | None | Wrist never goes above the shoulder |
| Veronica_made_04 | 59 | 70 (11) | 70 (11) |  |

**Shooter only, 480 px: 5/11 within ±3. A release is found on 6/11, and those 6 average 3.5 frames off (5 of them within ±3). The other 5 are refused with a reason instead of a wrong frame.** The crop still has a teammate or defender in view, so some refusals are the same wrong-person problem.


### Re-run on a Mac (official step-7 command, Apple M3 Pro)
`python -m ml.tools.eval_release ~/clips data/release_frames.csv`, after Path A, full broadcast frame:

| Clip | Quality | Hand label | Detected (error) | Note |
|---|---|---:|---|---|
| Veronica_made_05 | bad | 84 | 44 (40) |  |
| Kelvin_Huang_05_Missed | clean | 63 | None | Pose lost near the release |
| Veronica_made_03 | clean | 183 | None | Tracked person jumps / changes |
| Veronica_made_01 | clean | 56 | None | Wrist never goes above the shoulder |
| Veronica_missed_03 | clean | 83 | 96 (13) |  |
| Kelvin_Huang_08_Missed | clean | 96 | None | Tracked person jumps / changes |
| Anisha_Made_05 | bad | 77 | None | Video looks sideways |
| Rijul_missed_05 | bad | 71 | None | Video looks sideways |
| Veronica_missed_04 | bad | 31 | 14 (17) |  |
| Manoj_Missed_07 | clean | 115 | None | Tracked person jumps / changes |
| Freya_Made_7 | clean | 24 | None | Tracked person jumps / changes |
| Kelvin_Huang_04_Make | clean | 91 | None | Pose lost near the release |
| Kelvin_Huang_06_Make | clean | 182 | 2 (180) |  |
| Kelvin_Huang_09_Make | clean | 126 | 187 (61) |  |
| Veronica_made_04 | clean | 59 | None | Tracked person jumps / changes |

| Set (Mac, full frame) | Within ±3 | Release found | Avg error (found only) |
|---|---|---|---|
| Clean | 0/11 | 3/11 | 84.7 |
| Bad | 0/4 | 2/4 | 28.5 |
| All 15 | 0/15 | 5/15 | 62.2 |

The Mac and Linux runs differ clip by clip because MediaPipe's pose output isn't identical across machines, but the picture is the same: on the full broadcast frame the pose is usually on the wrong player. The shooter-only accuracy test (`test_clean_set_release_accuracy`) **passes on the Mac**, meaning at least 3/11 within ±3 and at most 7 refused (64/64 tests pass).

**Verdict:** when the pose is on the shooter, the release rule is within ±3 almost every time. The error is upstream, in who the pose model tracks, and in rotated or spliced footage. → **Path A:** stop tuning the release rule, make bad footage fail gracefully, and require "only the shooter in frame" when filming.
