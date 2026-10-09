from ml.recurring_mistake_detector import recurring

def make_session(knee_status="good"):
    return {
        "feedback": [
            {"checkpoint": "elbow_alignment", "angle": 90, "status": "good", "tip": "Great elbow alignment"},
            {"checkpoint": "knee_bend", "angle": 160, "status": knee_status, "tip": "Knee tip"},
        ]
    }


def test_no_mistakes_returns_empty_list():
    sessions = [make_session() for _ in range(4)]
    assert recurring(sessions) == []


def test_knee_flagged_in_3_of_4_sessions():
    sessions = [
        make_session("needs_work"),
        make_session("good"),
        make_session("needs_work"),
        make_session("needs_work"),
    ]
    result = recurring(sessions)
    assert len(result) == 1
    assert result[0]["checkpoint"] == "knee_bend"
    assert result[0]["count"] == 3