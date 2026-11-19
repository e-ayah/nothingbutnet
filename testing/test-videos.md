# NothingButNet Test Video Set


| Filename   | Drive Link                    | What It Tests                     | Expected Behavior                                                 | Quality |
| ---------- | ----------------------------- | --------------------------------- | ----------------------------------------------------------------- | ------- |
| Veronica_made_05.mp4 | [Drive link](https://drive.google.com/file/d/1ynlrgHDShBxonYZLEaJJgVHKs1SBpCi7/view?usp=sharing) | Normal, made free throw           | Detect the shooter's pose and analyze shooting form.              | bad — spliced intro (coach close-up + stats graphic before the shot) |
| Kelvin_Huang_05_Missed.mp4 | [Drive link](https://drive.google.com/file/d/1RaaWHXlHicsHjO8FDdzfNsuSBkjXfW6p/view?usp=sharing) | Normal, missed free throw         | Analyze shooting form regardless of shot outcome.                 | clean |
| Veronica_made_03.mp4 | [Drive link](https://drive.google.com/file/d/1GYXUX2ozwaapiZlMtym2Q6aoY8k1UTwh/view?usp=sharing) | Normal free throw                 | Correctly identify the shooter's release frame.                   | clean |
| Veronica_made_01.mp4 | [Drive link](https://drive.google.com/file/d/1TMWF79-U_bTuB4E0WyfauJdGcWZm3lCz/view?usp=sharing) | Normal free throw                 | Detect body landmarks and analyze shooting form.                  | clean |
| Veronica_missed_03.mp4 | [Drive link](https://drive.google.com/file/d/1t52Ob0YWCcpSVXLD9jRlPvJnN06MFYdW/view?usp=sharing) | Normal free throw | Analyze the shooter's form without assuming right-handedness.     | clean |
| Kelvin_Huang_08_Missed.mp4 | [Drive link](https://drive.google.com/file/d/1piHg8PNMNoSBFnGVs0Qz0cLQnRXvsaxS/view?usp=sharing) | Normal free throw                 | Identify the release frame in a clear video.                      | clean |
| Anisha_Made_05.mp4 | [Drive link](https://drive.google.com/file/d/1RBXy0qrVu-nUh2vgNUDB_E3UoIExTX11/view?usp=sharing) | Video rotated 90° and blurry                      | Handle the rotated orientation and attempt to detect the shooter's landmarks despite reduced image clarity. | bad — rotated 90° (pipeline ignores rotation metadata), blurry |
| Rijul_missed_05.mp4 | [Drive link](https://drive.google.com/file/d/1_s4wvRqENkFQycj-5kVqfy7MJXtlgTOC/view?usp=sharing) | Video rotated 90°, blurry, with a photographer's flash           | Handle the rotated orientation and changes in brightness from the flash; identify the release frame if it can be determined reliably.               | bad — rotated 90°, blurry, camera flash |
| Veronica_missed_04.mp4 | [Drive link](https://drive.google.com/file/d/1LBd76kukFGqgbuMD_h7ckSkUG6gyC8oL/view?usp=sharing) | Intro footage before the shot          | Identify the actual shooting sequence and correctly determine the ball's release frame, rather than labeling the introductory footage.                           | bad — spliced intro (player close-up before the shot) |
| Manoj_Missed_07.mp4 | [Drive link](https://drive.google.com/file/d/1dH9aVQhRGUT1DqPsOk3NWrNjwqujw8Vb/view?usp=sharing) | Cropped video frame            | Correctly detect and analyze the shooter even when the video frame is cropped.  | clean (zoomed/cropped, but whole body in frame and sharp) |
| Freya_Made_7.mp4 | [Drive link](https://drive.google.com/file/d/1Gg4w2ML4_R0-e9bPXFPSGj0JpNLxwwUW/view?usp=sharing) | WNBA free throw, wide side-front view | Correctly identify the release frame on clean footage. | clean |
| Kelvin_Huang_04_Make.mp4 | [Drive link](https://drive.google.com/file/d/1VVC8pMQ_LQoeIh8vaD6nh1TdqT01NH8T/view?usp=sharing) | NBA free throw, side view | Correctly identify the release frame on clean footage. | clean |
| Kelvin_Huang_06_Make.mp4 | [Drive link](https://drive.google.com/file/d/1Ily3ZQBfgiID0lmNxM5pKcJgROr5s_HW/view?usp=sharing) | NBA free throw, side view (flash after release) | Correctly identify the release frame on clean footage. | clean |
| Kelvin_Huang_09_Make.mp4 | [Drive link](https://drive.google.com/file/d/1nqNxQgIb6cgwh7hIyTabQB6_dvgqLla8/view?usp=sharing) | NBA free throw, wider side view | Correctly identify the release frame on clean footage. | clean |
| Veronica_made_04.mp4 | [Drive link](https://drive.google.com/file/d/1Nna6wMAb0X8BE_4aly9eiXwzZNM2woAC/view?usp=sharing) | WNBA free throw, side-front view | Correctly identify the release frame on clean footage. | clean |



**Quality** (Finals#04): `clean` = whole body + ball in frame, filmed from the side, sharp at release, one continuous take, normal speed, not rotated. Clips are picked on footage alone, before running the detector. `bad` clips stay in `data/release_frames.csv` to test how bad footage is handled.
