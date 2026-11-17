# NothingButNet ML pipeline

Turns a side-view free-throw clip into pose landmarks, a release-frame estimate, elbow/knee/shoulder measurements, rule-based feedback and an annotated MP4. The score is a form heuristic, not a trained probability that the shot goes in.

Follow [ML setup](../docs/setup.md#ml-setup-and-tests) with Python 3.11. MediaPipe must remain at `0.10.21`: the code uses `mp.solutions.pose`. Use NumPy 1.26.4 and one OpenCV distribution (the guide explains the headless swap).

```bash
# From the repository root with the virtual environment active:
python -m pytest ml/tests -q
python -m ml.analysis_pipeline /absolute/path/to/clip.mp4
```

The command prints JSON, an annotated temporary video path (or `None` for an undetected release), and runtime. It requires no API, database or Cloudinary account. The bundled test clips live in `ml/tests/data/`; the larger evaluation set requires access to the team's [video references](../testing/test-videos.md). Keep downloaded/generated videos outside Git.

```bash
# Evaluate against the existing answer key; all referenced clips must be available:
python -m ml.tools.eval_release /absolute/path/to/clips data/release_frames.csv
```

See [architecture](../docs/architecture.md#analysis-flow), [historical accuracy](../testing/reports/accuracy.md), [speed experiments](../docs/ml/speed.md), and the [project draft](../docs/writeups/project-writeup-draft.md). Finals #04 and #09–#11 will supply final accuracy/experiment numbers; do not describe old measurements or form-score examples as final validation.
