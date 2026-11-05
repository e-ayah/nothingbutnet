from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import ShotSession, AnalysisResult
from services.deps import get_current_user
from schemas.progress import ProgressResponse
from services.summary import improvement_summary

router = APIRouter()

ANGLE_KEYS = ["elbow_angle", "knee_angle", "shoulder_angle"]


@router.get("", response_model=ProgressResponse)
def get_progress(
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    results = (
        db.query(ShotSession, AnalysisResult)
        .join(AnalysisResult, AnalysisResult.session_id == ShotSession.id)
        .filter(
            ShotSession.user_id == user.id,
            ShotSession.status == "done",
        )
        .order_by(ShotSession.created_at.asc())
        .all()
    )

    sessions = []
    trends = {
        "elbow_angle": [],
        "knee_angle": [],
        "shoulder_angle": [],
    }

    for session, analysis in results:
        angles = {
            "elbow_angle": analysis.elbow_angle,
            "knee_angle": analysis.knee_angle,
            "shoulder_angle": analysis.shoulder_angle,
        }

        # Skip sessions with missing angle measurements
        if any(value is None for value in angles.values()):
            continue

        session_data = {
            "session_id": str(session.id),
            "created_at": session.created_at.isoformat(),
            "angles": angles,
            "score": session.overall_score,
        }

        sessions.append(session_data)

        for key in ANGLE_KEYS:
            trends[key].append(angles[key])

    summary = improvement_summary(sessions)

    return {
        "sessions": sessions,
        "trends": trends,
        "improvement_summary": summary,
    }


@router.get("/ping")
def ping():
    return {"router": "progress"}