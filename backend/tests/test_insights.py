
from types import SimpleNamespace
from unittest.mock import MagicMock

from routers.insights import recurring


def make_session(session_id):
    return SimpleNamespace(id=session_id)


def make_feedback(session_id, status):
    return SimpleNamespace(
        session_id=session_id,
        checkpoint="elbow_alignment",
        status=status,
        tip=f"Tip from session {session_id}"
    )


def run_recurring_test(sessions, feedback):
    # Create a fake database
    db = MagicMock()

    # Separate the two database queries
    session_query = MagicMock()
    feedback_query = MagicMock()

    db.query.side_effect = [session_query, feedback_query]

    # Configure the session query
    session_query.filter.return_value.order_by.return_value.limit.return_value.all.return_value = sessions

    # Configure the feedback query
    feedback_query.filter.return_value.all.return_value = feedback

    # Create a fake logged-in user
    user = SimpleNamespace(id=1)

    # Run the actual endpoint function
    return recurring(db=db, user=user)


def test_four_out_of_five_returns_elbow():
    # Create five completed sessions
    sessions = [
        make_session(5),
        make_session(4),
        make_session(3),
        make_session(2),
        make_session(1)
    ]

    # Four sessions need elbow work
    feedback = [
        make_feedback(5, "needs_work"),
        make_feedback(4, "needs_work"),
        make_feedback(3, "needs_work"),
        make_feedback(2, "needs_work"),
        make_feedback(1, "good")
    ]

    result = run_recurring_test(sessions, feedback)

    assert len(result) == 1
    assert result[0]["checkpoint"] == "elbow_alignment"
    assert result[0]["label"] == "Elbow"
    assert result[0]["count"] == 4
    assert result[0]["out_of"] == 5
    assert result[0]["latest_tip"] == "Tip from session 5"


def test_two_out_of_five_does_not_return_elbow():
    # Create five completed sessions
    sessions = [
        make_session(5),
        make_session(4),
        make_session(3),
        make_session(2),
        make_session(1)
    ]

    # Only two sessions need elbow work
    feedback = [
        make_feedback(5, "needs_work"),
        make_feedback(4, "needs_work"),
        make_feedback(3, "good"),
        make_feedback(2, "good"),
        make_feedback(1, "good")
    ]

    result = run_recurring_test(sessions, feedback)

    assert result == []


def test_fewer_than_three_sessions_returns_empty():
    # Only two completed sessions
    sessions = [
        make_session(2),
        make_session(1)
    ]

    feedback = [
        make_feedback(2, "needs_work"),
        make_feedback(1, "needs_work")
    ]

    result = run_recurring_test(sessions, feedback)

    assert result == []
