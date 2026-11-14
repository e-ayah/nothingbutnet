
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import patch
from types import SimpleNamespace
from fastapi import HTTPException

from routers.compare import router, load
from services.deps import get_current_user, get_db


app = FastAPI()
app.include_router(router, prefix="/sessions")

# Fake logged-in user
fake_user = SimpleNamespace(id="user123")


def override_user():
    return fake_user


def override_db():
    yield None


app.dependency_overrides[get_current_user] = override_user
app.dependency_overrides[get_db] = override_db

client = TestClient(app)


def make_session(session_id, score, elbow, knee, shoulder):
    return {
        "session_id": session_id,
        "created_at": "2026-11-07T12:00:00",
        "video_url": "test.mp4",
        "annotated_video_url": "annotated.mp4",
        "angles": {
            "elbow_angle": elbow,
            "knee_angle": knee,
            "shoulder_angle": shoulder,
        },
        "score": score,
    }


def test_compare_two_sessions():
    session_a = make_session("1", 78, 82, 155, 40)
    session_b = make_session("2", 86, 90, 165, 55)

    with patch("routers.compare.load", side_effect=[session_a, session_b]):
        response = client.get("/sessions/compare?a=1&b=2")

    assert response.status_code == 200

    data = response.json()

    assert data["a"]["session_id"] == "1"
    assert data["b"]["session_id"] == "2"

    assert data["changes"]["elbow_angle"] == 8
    assert data["changes"]["knee_angle"] == 10
    assert data["changes"]["shoulder_angle"] == 15
    assert data["changes"]["score"] == 8


def test_other_users_session_returns_404():
    def fake_load(db, session_id, user):
        if session_id == "other_user_session":
            raise HTTPException(
                status_code=404,
                detail="Session not found"
            )

        return make_session("1", 78, 82, 155, 40)

    with patch("routers.compare.load", side_effect=fake_load):
        response = client.get(
            "/sessions/compare?a=1&b=other_user_session"
        )

    assert response.status_code == 404


def test_missing_angle():
    session_a = make_session("1", 78, None, 155, 40)
    session_b = make_session("2", 86, 90, 165, 55)

    with patch("routers.compare.load", side_effect=[session_a, session_b]):
        response = client.get("/sessions/compare?a=1&b=2")

    assert response.status_code == 200
    assert response.json()["changes"]["elbow_angle"] is None
