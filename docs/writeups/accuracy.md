# How accurate is release detection? (Finals#04)

## Problem
The release-frame detector averaged about 22 frames off on the 10-clip answer key. That key mixed in junk footage: a spliced intro with a different person, rotated or blurry clips, and a flash. We didn't know whether the detector was bad or the test set was. "How accurate is it?" is the first question judges ask, so we needed an honest number before spending a sprint "fixing" detection.

## What we found
- **Clean answer key.** 11 clips picked on footage alone, before running the detector: whole body and ball in frame, side view, sharp at the release, one continuous take, not rotated. Each is hand-labeled with one rule: the first frame where there's a gap between ball and fingertips. Bad clips are flagged in `testing/test-videos.md` and kept for testing failure handling.
- **The release rule isn't the main problem.** All our test clips are NBA/WNBA broadcasts with 8 to 10 people in view, and MediaPipe Pose tracks one person, often a bystander. Every time the pose *was* on the shooter, the detected release was **2 frames** off. With only the shooter in view, the existing rule gets **8 of 11 clips within ±3 frames, averaging 3.0 frames off**.

![Pose locked onto the wrong player](img/wrong_person_Veronica_made_01.jpg)

- **So we took Path A.** The release rule stays as it is. The detector now **refuses instead of guessing** and returns `None` plus a filming tip when:
  - the video looks sideways (median shoulder→hip angle more than 45° from vertical), usually a phone clip whose rotation flag the decoder ignores
  - the tracked body jumps more than 2.5 torso lengths in one frame, or changes size more than 1.8×, *and stays there*, which means a cut or a switch to another person. One-frame glitches that snap back are ignored.
  - more than 5 frames of pose are missing within ±8 frames of the release

  I tuned the jump threshold on a Linux run (49 detections). At 2.5 it refused 1 of 19 correct answers and 7 of 30 wrong ones. At 1.5 it refused 4 correct answers.

## Numbers
All Finals numbers are from a MacBook Pro (M3 Pro). The full per-clip tables are in `testing/reports/accuracy.md`.

| Footage | Within ±3 | Release found | Avg error when found |
|---|---|---|---|
| Old 10-clip key, Sixers#02 | 2/10 | 9/10 | 22.0 |
| Clean clips, full broadcast frame, before → after | 2/11 → 0/11 | 10 → 3 | 62.0 → 84.7 |
| **Clean clips, shooter only, 480 px (server size), before (rule only)** | **8/11** | **10/11** | **3.0** |
| **Clean clips, shooter only, 480 px, after (Path A)** | **6/11** | **8/11** | **3.4** |
| Bad clips (rotated / spliced), full size, before → after | 0/4 → 0/4 | 4 → 2 | 25.8 → 28.5 |

The two rotated clips are now refused instead of being 19 to 27 frames off. The spliced intros still slip through: Veronica_made_05 returns a frame 40 off, and Veronica_missed_04 one 17 off. Path A also refuses 2 correct answers on shooter-only footage (Kelvin_Huang_05 and Kelvin_Huang_09), because another player is still in the crop.

![Accuracy by sprint](img/accuracy_progress.png)
![Per-clip error, shooter only](img/per_clip_error.png)

**Debug plots** (Linux run; elbow angle and wrist height; dashed = hand label, orange = detected):

![Clean hit](img/debug_Freya_Made_7.png)
![Wrong player tracked](img/debug_Veronica_made_01.png)
![Rotated clip refused](img/debug_Anisha_Made_05.png)

## What bad footage does now
| Footage | Result |
|---|---|
| Rotated 90° | `None`: "The video looks sideways…" |
| Cut / someone else takes over | `None`: "The tracked person jumps or changes mid-clip…" |
| Pose lost around the release | `None`: "Pose lost near the release…" |

**Filming requirements** (for Finals#03's validator and the onboarding tips):
1. Film from the side, with the shooting arm toward the camera.
2. Keep your whole body and the ball in frame for the entire shot.
3. **Only the shooter in frame.** No teammates or defenders in view.
4. One continuous take with no intro or cuts. Don't rotate the phone mid-recording.
5. Normal speed (no slow-mo), steady phone, good light, so the fingertips are sharp at the release.

## What's left
- **Pose tracks the wrong person in crowded footage.** That's the biggest remaining error, and a person-switch is only caught if it happens *mid-clip*. A clip locked onto a bystander from the start still returns a wrong frame (Freya_Made_7 full frame: 97 off). Next step: run MediaPipe's multi-person `PoseLandmarker` and pick the body whose wrist rises above its head.
- **We have no real "one person, side-on" phone clips.** Every clip in the Drive is broadcast footage, and the shooter-only numbers come from crops of it. A short session filming teammates would give the true number.
- **The splice and intro check misses intros with no full-body pose.** Veronica_made_05 and Veronica_missed_04 open on close-ups and still return a frame (40 and 17 off).
- **Path A refuses some good clips.** 2 of 11 shooter-only clips were refused because a second player is in view. Raise `SPLICE_JUMP` if fewer refusals matter more.
- **Results vary by machine.** MediaPipe output differs between Mac and Linux, by a few frames and sometimes between found and None. The accuracy test allows 2 clips of slack and passes on both.
