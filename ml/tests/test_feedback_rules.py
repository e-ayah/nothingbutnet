from ml.feedback_rules import ANGLE_RANGES, evaluate_form
from ml.tips import TIPS

IN_RANGE = {"elbow_angle": 90, "knee_angle": 150, "shoulder_angle": 60}

def get_item(result, angle_key):
    checkpoint = ANGLE_RANGES[angle_key]["checkpoint"]
    for item in result["feedback"]:
        if item["checkpoint"] == checkpoint:
            return item

def test_all_in_range_all_good():
    result = evaluate_form(IN_RANGE)
    assert len(result["feedback"]) == 3
    assert all(item["status"] == "good" for item in result["feedback"])
    assert result["overall_score"] == 100

def test_elbow_60_needs_work():
    result = evaluate_form({**IN_RANGE, "elbow_angle": 60})
    assert get_item(result, "elbow_angle")["status"] == "needs_work"
    assert get_item(result, "knee_angle")["status"] == "good"
    assert get_item(result, "shoulder_angle")["status"] == "good"
    assert result["overall_score"] == 50

def test_elbow_exactly_85_is_good():
    result = evaluate_form({**IN_RANGE, "elbow_angle": 85})
    assert get_item(result, "elbow_angle")["status"] == "good"
    assert result["overall_score"] == 100

def test_elbow_exactly_100_is_good():
    result = evaluate_form({**IN_RANGE, "elbow_angle": 100})
    assert get_item(result, "elbow_angle")["status"] == "good"
    assert result["overall_score"] == 100

def test_missing_angle_is_skipped():
    result = evaluate_form({**IN_RANGE, "knee_angle": None})
    assert get_item(result, "knee_angle") is None
    assert len(result["feedback"]) == 2
    assert result["overall_score"] == 100

def test_low_elbow_uses_too_low_tip():
    result = evaluate_form({**IN_RANGE, "elbow_angle": 70})
    assert get_item(result, "elbow_angle")["tip"] == TIPS["elbow_alignment"]["too_low"]

def test_high_knee_uses_too_high_tip():
    result = evaluate_form({**IN_RANGE, "knee_angle": 179})
    assert get_item(result, "knee_angle")["tip"] == TIPS["knee_bend"]["too_high"]

def test_good_shoulder_uses_good_tip():
    result = evaluate_form({**IN_RANGE, "shoulder_angle": 60})
    assert get_item(result, "shoulder_angle")["tip"] == TIPS["shoulder_position"]["good"]
    