from ml.analysis_pipeline import analyze


def test_analyze():
    result = analyze("x.mp4")

    assert result["session_id"] is None
    assert "release_frame" in result
    assert "angles" in result
    assert "feedback" in result
    assert "overall_score" in result
    assert "annotated_video_url" in result
    assert "processed_at" in result