from ml.trend_analyzer import trends

# Sixers#02: elbow values shifted +65 to fit the new elbow range (115-165)


def make_session(elbow_angle):
    return {
        "angles": {
            "elbow_angle": elbow_angle,
        }
    }


def test_improving():
    sessions = [
        make_session(175),
        make_session(170),
        make_session(167),
        make_session(163),
    ]

    result = trends(sessions)

    assert result["labels"]["elbow_angle"] == "improving"


def test_declining():
    sessions = [
        make_session(163),
        make_session(167),
        make_session(170),
        make_session(175),
    ]

    result = trends(sessions)

    assert result["labels"]["elbow_angle"] == "declining"


def test_flat():
    sessions = [
        make_session(155),
        make_session(157),
        make_session(160),
        make_session(163),
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
        make_session(175),
        make_session(None),
        make_session(170),
        make_session(167),
        make_session(163),
    ]

    result = trends(sessions)

    assert result["labels"]["elbow_angle"] == "improving"
    assert result["trends"]["elbow_angle"] == [175, 170, 167, 163]

def test_session_without_angles_is_skipped():
    # processing/failed sessions have angles=None
    sessions = [
        make_session(175),
        {"angles": None},
        make_session(170),
        make_session(167),
    ]

    result = trends(sessions)

    assert result["trends"]["elbow_angle"] == [175, 170, 167]
    assert result["labels"]["elbow_angle"] == "improving"


def test_ranges_match_feedback_rules():
    from ml.feedback_rules import ANGLE_RANGES
    from ml.trend_analyzer import RANGES
    assert RANGES == {k: (v["min"], v["max"]) for k, v in ANGLE_RANGES.items()}
