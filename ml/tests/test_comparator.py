from ml.session_comparator import compare

def make_session(elbow = None, knee = 160, shoulder = 60):
    return {"angles": {"elbow_angle": elbow, "knee_angle": knee, "shoulder_angle": shoulder}}

def get(result, checkpoint):
    for item in result:
        if item["checkpoint"] == checkpoint:
            return item

def test_elbow_70_to_90_is_better():
    result = compare(make_session(elbow=70), make_session(elbow=90))
    assert get(result, "elbow_angle")["direction"] == "better"

def test_elbow_95_to_110_is_worse():
    result = compare(make_session(elbow=95), make_session(elbow=110))
    assert get(result, "elbow_angle")["direction"] == "worse"

def test_elbow_92_to_92_5_is_same():
    result = compare(make_session(elbow=92), make_session(elbow=92.5))
    assert get(result, "elbow_angle")["direction"] == "same"

def test_elbow_None_to_90_is_unknown():
    result = compare(make_session(elbow=None), make_session(elbow=90))
    assert get(result, "elbow_angle")["direction"] == "unknown"

def test_session_without_angles_is_unknown():
    # processing/failed sessions have angles=None
    result = compare({"angles": None}, make_session(elbow=90))
    assert all(item["direction"] == "unknown" for item in result)

def test_ranges_match_feedback_rules():
    from ml.feedback_rules import ANGLE_RANGES
    from ml.session_comparator import RANGES
    assert RANGES == {k: (v["min"], v["max"]) for k, v in ANGLE_RANGES.items()}
