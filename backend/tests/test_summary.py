from services.summary import improvement_summary


def make_session(elbow, knee, shoulder):
    return {
        "angles": {
            "elbow_angle": elbow,
            "knee_angle": knee,
            "shoulder_angle": shoulder,
        }
    }


def test_elbow_improves():
    sessions = [
        make_session(70, 160, 60),
        make_session(90, 160, 60),
    ]

    result = improvement_summary(sessions)

    assert "elbow angle improved" in result


def test_knee_gets_worse():
    sessions = [
        make_session(90, 160, 60),
        make_session(90, 190, 60),
    ]

    result = improvement_summary(sessions)

    assert "knee bend moved farther from the ideal range" in result


def test_steady():
    sessions = [
        make_session(90, 160, 60),
        make_session(90, 160, 60),
    ]

    result = improvement_summary(sessions)

    assert result == "Your form is holding steady. Keep shooting!"


def test_fewer_than_two_sessions():
    sessions = [
        make_session(90, 160, 60),
    ]

    result = improvement_summary(sessions)

    assert result == "Analyze at least 2 shots to see your progress."


def test_none_values():
    sessions = [
        make_session(None, 160, 60),
        make_session(90, 160, 60),
    ]

    result = improvement_summary(sessions)

    assert "knee bend" not in result or "elbow angle" in result