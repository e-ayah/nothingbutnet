from schemas.auth import SignupRequest, LoginRequest, AuthResponse
from schemas.analysis import AnalysisResponse
from schemas.sessions import UploadResponse, SessionSummary, SessionDetail
from schemas.progress import ProgressResponse
from schemas.goals import GoalCreate, GoalOut
# import everything in order to test everything!

"""
tests for the pydantic schemas in backend/schemas
each test builds a model from sample data. if the field names or types
don't match the schema, pydantic raises an error and the test fails

analysis_example is copied from the POST /analysis/analyze response
in the api contract
the trends and improvement_summary values in test_progress come from
the GET /progress example in the api contract
the other values (emails, ids like "g1", dates) are sample values i made
up, because the contract only lists field names for those endpoints

i added test_auth, test_sessions, and test_goals so every model gets built
at least once, since the ticket's "done when" says a test builds each one
"""

analysis_example = {
    "session_id": "abc123",
    "release_frame": 45,
    "angles": {"elbow_angle": 92.3, "knee_angle": 165.1, "shoulder_angle": 58.7},
    "feedback": [
        {"checkpoint": "elbow_alignment", "angle": 92.3, "status": "good", "tip": "Great elbow alignment"}
    ],
    "overall_score": 67,
    "annotated_video_url": "https://cloudinary.com/...",
    "processed_at": "2026-09-15T10:30:00Z",
}


def test_analysis_response():
    result = AnalysisResponse(**analysis_example)
    assert result.session_id == "abc123"
    assert result.angles.elbow_angle == 92.3


def test_auth():
    SignupRequest(email="a@b.com", password="pw", name="Sam")
    LoginRequest(email="a@b.com", password="pw")
    AuthResponse(user_id="1", token="abc")


def test_sessions():
    UploadResponse(session_id="abc123", video_url="x", status="processing")
    SessionSummary(session_id="abc123", created_at="2026-09-15", overall_score=67, status="done")
    detail = SessionDetail(
        session_id="abc123", video_url="x", annotated_video_url="y",
        score=67, status="processing",
    )
    assert detail.angles is None
    # while processing there's no score or annotated video yet
    pending = SessionDetail(session_id="abc123", video_url="x", status="processing")
    assert pending.score is None
    SessionSummary(session_id="abc123", created_at="2026-09-15", status="processing")


def test_progress():
    ProgressResponse(
        sessions=[{
            "session_id": "abc123", "created_at": "2026-09-15",
            "angles": analysis_example["angles"], "score": 67,
        }],
        trends={
            "elbow_angle": [92.3, 88.1, 94.5],
            "knee_angle": [165.1, 168.2, 170.0],
            "shoulder_angle": [58.7, 61.2, 63.0],
        },
        improvement_summary="Your elbow angle improved 2.2 degrees",
    )


def test_goals():
    GoalCreate(checkpoint="elbow_alignment", target_angle=90)
    GoalOut(id="g1", checkpoint="elbow_alignment", target_angle=90, current_angle=85.5, progress=0.9)