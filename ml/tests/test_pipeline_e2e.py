
import os
from pathlib import Path

import pytest

from ml.analysis_pipeline import analyze


DEFAULT = Path(__file__).parent / "data" / "pose_clip.mp4"
CLIP = os.environ.get("NBN_TEST_CLIP", str(DEFAULT))


@pytest.mark.skipif(
    not Path(CLIP).expanduser().exists(),
    reason="test clip not found"
)
def test_full_pipeline_on_a_real_clip():
    result, annotated = analyze(str(Path(CLIP).expanduser()))

    assert {"angles", "feedback", "overall_score"} <= set(result)
    assert 0 <= result["overall_score"] <= 100
    assert Path(annotated).exists()
