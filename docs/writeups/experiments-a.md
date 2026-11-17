# Finals #09 Part 2 — do the app's form rules match real makes?

## Problem
The app tells shooters whether their elbow, knee, and shoulder angles at release are "good" or "needs work," and gives an overall form score. Nobody had actually checked whether shots the app calls good-form really go in more often than ones it flags.

## What we built / found
Using `data/features.csv` (89 shots, built from 185 hand-labeled clips — 96 were skipped because MediaPipe didn't detect a pose at the release frame), we ran every shot's release-frame angles through the app's own `evaluate_form` function and compared make rates between "good" and "needs_work" shots for each checkpoint, then tested whether made shots score higher overall using a permutation test (10,000 shuffles).

All three checkpoints now point the same direction: shots the app calls "good" on a checkpoint go in more often than shots it flags "needs_work." Made shots scored 6.6 points higher on average than missed shots — a much bigger gap than the earlier partial-sample result, though a permutation test says it still isn't significant at the conventional threshold (p = 0.289).

Every one of the 11 players in this dataset has a mix of makes and misses, so this result isn't just re-measuring "which player shot it" the way the earlier 21-shot sample was.

## Numbers
- 89 shots, 47 made / 42 missed, 11 players
- elbow_alignment: good 0.60 make rate (n=53) vs needs_work 0.42 (n=36)
- knee_bend: good 0.61 make rate (n=56) vs needs_work 0.39 (n=33)
- shoulder_position: good 0.56 make rate (n=71) vs needs_work 0.39 (n=18)
- made shots score 6.6 points higher on average, p = 0.289 (not significant at p < 0.05, but a much larger and more consistent effect than the earlier confounded partial result)

## Pictures
![Make rate by checkpoint status](img/experiments_a_checkpoint_make_rate.png)

## Caveats
- Sample sizes per player are uneven (2 to 14 shots), and total n (89) is still modest for a permutation test, so treat the p-value as suggestive rather than conclusive.
- 96 of 185 labeled clips were dropped because the pose pipeline couldn't detect a pose at the marked release frame — if those failures aren't random (e.g. biased toward certain shooting forms or camera angles), that could skew the comparison.
- One labeling inconsistency was caught and fixed during this pass: Veronica's original label file used "Kelvin_Huang" for his made clips but "Kelvin" for his missed clips, which would have falsely looked like a second, fully-confounded player.

## What's left
With the confound resolved, the honest next step is more data: a bigger, more balanced sample (especially for players at the low end like Rijul at n=2) would make the permutation test more trustworthy. Whoever owns Finals #10/#11 (the classifier experiments) can now use this same 89-row `features.csv` instead of the original 8-row version they were blocked on.
