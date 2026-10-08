# Labeling Guide

We train only on broadcast footage of professional basketball players, and will follow the guidelines below for usable clips.

As our model is based on professionals, the outcome (made/missed) is labeled separately from whether the form is deemed 'good' or 'needs work.' This is because even if they missed, pros usually still have good form.

Thus, expect most clips to be 'good', and 'needs_work' will only be used for visible flaws, and 'unsure' otherwise.

## Columns in `data/labels_template.csv`

| Column | Allowed values |
|---|---|
| `filename` | clip file name |
| `uploader` | who added the clip |
| `outcome` | `made` / `missed` |
| `usable` | `y` / `n` (see checklist below) |
| `unusable_reason` | short note, only if `usable` is `n` |
| `form_label` | `good` / `needs_work` / `unsure` |
| `form_reason` | short note on why |

## Usability Checklist

- Camera angle is filmed from the side that the player's shooting (dominant) hand is fully shown
- Full body is visible from feet to hands, with nothing cropping the player
- Steady footage with no cuts, zooms, slow-motion replays, or camera pans mid-clip
- The player should clearly be in frame, with little to no blocking from other objects or people
- The clip should be in good lighting and no dark silhouettes
- The motion should be fully seen from the set position to the release and follow-through  

### Optimal angles for Good Form

- Elbow alignment needs to be 85–100° angle
- Knee bend needs to be at 150–175° angle 
- Shoulder angle is at a 45–75° angle

-----------------------------------------------------------------------------------------------------------

### 1: Good freethrow

https://www.youtube.com/watch?v=MW7bXa8K3bY 

In the first clip of Jimmy Butler's free throw, his form is within the optimal angles in terms of elbow alignment, knee bend, and shoulder angle.  

### 2: Bad freethrow

https://www.reddit.com/r/nba/s/nPZjs7BcT5

In this clip of William Kyle's free throw, he shoots his freethrow at a straight angle, with no bend in his elbow. 