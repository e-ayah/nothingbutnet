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
