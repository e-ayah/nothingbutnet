import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import ShotSession, AnalysisResult, FeedbackItem
from schemas.sessions import SessionSummary, SessionDetail
from schemas.analysis import Angles, FeedbackItem as FeedbackItemSchema
from services.deps import get_current_user

router = APIRouter()

@router.get("/ping")
def ping():
    return {"router": "sessions"}

@router.get("", response_model=list[SessionSummary])
def list_sessions(user=Depends(get_current_user), db: Session = Depends(get_db)):
    rows = (db.query(ShotSession)
              .filter(ShotSession.user_id == user.id)
              .order_by(ShotSession.created_at.desc())
              .all())
    return [SessionSummary(session_id=str(r.id), created_at=r.created_at.isoformat(),
                           overall_score=r.overall_score, status=r.status) for r in rows]


@router.get("/{session_id}", response_model=SessionDetail)
def get_session(session_id: uuid.UUID, user=Depends(get_current_user), db: Session = Depends(get_db)):
    s = db.get(ShotSession, session_id)
    if s is None or s.user_id != user.id:
        raise HTTPException(status_code=404, detail="Session not found")
    result = (db.query(AnalysisResult)
                .filter(AnalysisResult.session_id == s.id)
                .first())
    items = (db.query(FeedbackItem)
               .filter(FeedbackItem.session_id == s.id)
               .all())

    # processing (or failed) sessions have no analysis yet, so these stay None
    angles = None
    feedback = None
    if result is not None:
        angles = Angles(
            elbow_angle=result.elbow_angle,
            knee_angle=result.knee_angle,
            shoulder_angle=result.shoulder_angle,
        )
        feedback = [
            FeedbackItemSchema(
                checkpoint=i.checkpoint_name,
                angle=i.angle_value,
                status=i.status,
                tip=i.tip,
            )
            for i in items
        ]

    return SessionDetail(
        session_id=str(s.id),
        video_url=s.video_url,
        annotated_video_url=s.annotated_video_url,
        angles=angles,
        feedback=feedback,
        score=s.overall_score,
        status=s.status,
        error=s.error,
    )
