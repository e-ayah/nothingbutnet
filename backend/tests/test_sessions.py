
from datetime import datetime
from uuid import UUID

from models import ShotSession, User


def test_new_user_has_no_sessions(client, token):
    response = client.get(
        "/sessions",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.json() == []


def test_cannot_read_another_users_session(client, token, db_session):
    # Create a second user.
    signup = client.post(
        "/auth/signup",
        json={
            "email": "other@test.com",
            "password": "password123",
            "name": "Other User"
        }
    )
    assert signup.status_code == 200

    other_user_id = UUID(signup.json()["user_id"])

    # Create a session belonging to the second user.
    session = ShotSession(
        user_id=other_user_id,
        video_url="test_video.mp4",
        status="done",
        overall_score=85.0
    )

    db_session.add(session)
    db_session.commit()
    db_session.refresh(session)

    # First user attempts to access the second user's session.
    response = client.get(
        f"/sessions/{session.id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 404


def test_sessions_returned_newest_first(client, token, db_session):
    # Find the authenticated user's ID.
    me = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    user_id = UUID(me.json()["id"])

    # Create an older session.
    older = ShotSession(
        user_id=user_id,
        video_url="older.mp4",
        status="done",
        overall_score=70.0,
        created_at=datetime(2025, 1, 1)
    )

    # Create a newer session.
    newer = ShotSession(
        user_id=user_id,
        video_url="newer.mp4",
        status="done",
        overall_score=90.0,
        created_at=datetime(2025, 1, 2)
    )

    db_session.add_all([older, newer])
    db_session.commit()

    response = client.get(
        "/sessions",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200

    sessions = response.json()

    assert len(sessions) == 2
    assert sessions[0]["session_id"] == str(newer.id)
    assert sessions[1]["session_id"] == str(older.id)


def test_made_answer_is_returned_when_reopening_a_session(client, token, db_session):
    # 'Did it go in?' must still show the player's answer when Results is opened again.
    headers = {"Authorization": f"Bearer {token}"}
    me = client.get("/auth/me", headers=headers).json()
    session = ShotSession(user_id=UUID(me["id"]), video_url="test_video.mp4", status="done")
    db_session.add(session)
    db_session.commit()
    db_session.refresh(session)

    assert client.get(f"/sessions/{session.id}", headers=headers).json()["made"] is None
    assert client.patch(f"/sessions/{session.id}", json={"made": True}, headers=headers).status_code == 200
    assert client.get(f"/sessions/{session.id}", headers=headers).json()["made"] is True
