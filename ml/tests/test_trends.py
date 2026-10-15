from ml.trend_analyzer import trends


def make_session(elbow_angle):
    return {
        "angles": {
            "elbow_angle": elbow_angle,
        }
    }


def test_improving():
    sessions = [
        make_session(110),
        make_session(105),
        make_session(102),
        make_session(98),
    ]

    result = trends(sessions)

    assert result["labels"]["elbow_angle"] == "improving"


def test_declining():
    sessions = [
        make_session(98),
        make_session(102),
        make_session(105),
        make_session(110),
    ]

    result = trends(sessions)

    assert result["labels"]["elbow_angle"] == "declining"


def test_flat():
    sessions = [
        make_session(90),
        make_session(92),
        make_session(95),
        make_session(98),
    ]

    result = trends(sessions)

    assert result["labels"]["elbow_angle"] == "flat"


def test_not_enough_data():
    sessions = [
        make_session(90),
        make_session(95),
    ]

    result = trends(sessions)

    assert result["labels"]["elbow_angle"] == "not enough data"


def test_none_value_is_skipped():
    sessions = [
        make_session(110),
        make_session(None),
        make_session(105),
        make_session(102),
        make_session(98),
    ]

    result = trends(sessions)

    assert result["labels"]["elbow_angle"] == "improving"
    assert result["trends"]["elbow_angle"] == [110, 105, 102, 98]

def test_session_without_angles_is_skipped():
    # processing/failed sessions have angles=None
    sessions = [
        make_session(110),
        {"angles": None},
        make_session(105),
        make_session(102),
    ]

    result = trends(sessions)

    assert result["trends"]["elbow_angle"] == [110, 105, 102]
    assert result["labels"]["elbow_angle"] == "improving"


def test_ranges_match_feedback_rules():
    from ml.feedback_rules import ANGLE_RANGES
    from ml.trend_analyzer import RANGES
    assert RANGES == {k: (v["min"], v["max"]) for k, v in ANGLE_RANGES.items()}
