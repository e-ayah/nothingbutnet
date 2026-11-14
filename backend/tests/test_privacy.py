
import pytest

from models import User, ShotSession, AnalysisResult
from services.security import hash_password, create_access_token


@pytest.fixture
def privacy_data(client, db_session):
    # Create two separate users.
    user_a = User(
        email="usera@test.com",
        password_hash=hash_password("password123"),
        name="User A",
        username="user_a",
    )
    user_b = User(
        email="userb@test.com",
        password_hash=hash_password("password123"),
        name="User B",
        username="user_b",
    )

    db_session.add_all([user_a, user_b])
    db_session.flush()

    # Create two sessions belonging to User A.
    session_a1 = ShotSession(
        user_id=user_a.id,
        video_url="https://example.com/video1.mp4",
        status="done",
        overall_score=80,
    )
    session_a2 = ShotSession(
        user_id=user_a.id,
        video_url="https://example.com/video2.mp4",
        status="done",
        overall_score=85,
    )

    db_session.add_all([session_a1, session_a2])
    db_session.flush()

    # Add analysis results so the sessions can be used for comparisons.
    for session in [session_a1, session_a2]:
        db_session.add(
            AnalysisResult(
                session_id=session.id,
                elbow_angle=90,
                knee_angle=160,
                shoulder_angle=60,
                release_frame=50,
            )
        )

    db_session.commit()

    return {
        "user_a_session": session_a1,
        "user_a_session_2": session_a2,
        "token_b": create_access_token(user_b.id),
    }


def test_user_cannot_view_another_users_session(client, privacy_data):
    session_id = privacy_data["user_a_session"].id

    response = client.get(
        f"/sessions/{session_id}",
        headers={"Authorization": f"Bearer {privacy_data['token_b']}"},
    )

    assert response.status_code == 404


def test_user_cannot_update_another_users_session(client, db_session, privacy_data):
    session = privacy_data["user_a_session"]

    response = client.patch(
        f"/sessions/{session.id}",
        json={"made": True},
        headers={"Authorization": f"Bearer {privacy_data['token_b']}"},
    )

    assert response.status_code == 404

    db_session.refresh(session)
    assert session.made is None


def test_user_cannot_compare_another_users_sessions(client, privacy_data):
    session_a = privacy_data["user_a_session"]
    session_b = privacy_data["user_a_session_2"]

    response = client.get(
        "/sessions/compare",
        params={"a": str(session_a.id), "b": str(session_b.id)},
        headers={"Authorization": f"Bearer {privacy_data['token_b']}"},
    )

    assert response.status_code == 404

def test_non_video_upload_is_rejected(client, privacy_data):
    response = client.post(
        "/sessions/upload",
        files={"file": ("test.txt", b"hello", "text/plain")},
        headers={"Authorization": f"Bearer {privacy_data['token_b']}"},
    )

    assert response.status_code == 400

def test_sessions_require_authentication(client):
    response = client.get("/sessions")
    assert response.status_code == 401


def test_invalid_token_is_rejected(client):
    response = client.get(
        "/sessions",
        headers={"Authorization": "Bearer fake-invalid-token"},
    )
    assert response.status_code == 401

def test_invalid_user_id_in_token_is_rejected(client):
    bad_token = create_access_token("not-a-valid-uuid")

    response = client.get(
        "/sessions",
        headers={"Authorization": f"Bearer {bad_token}"},
    )

    assert response.status_code == 401
