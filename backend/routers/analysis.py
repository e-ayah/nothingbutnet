import uuid

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import get_db
from models import ShotSession, AnalysisResult, FeedbackItem
from schemas.analysis import AnalysisResponse
from services.deps import get_current_user
from services import ml_pipeline

router = APIRouter()


@router.get("/ping")
def ping():
    return {"router": "analysis"}


class AnalyzeRequest(BaseModel):
    session_id: str
    video_url: str


@router.post("/analyze", response_model=AnalysisResponse)
def analyze(
    request: AnalyzeRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    try:
        session_uuid = uuid.UUID(request.session_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Session not found")

    session = db.query(ShotSession).filter(
        ShotSession.id == session_uuid,
        ShotSession.user_id == current_user.id,
    ).first()
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")

    try:
        result = ml_pipeline.run(request.video_url, request.session_id)

        analysis = AnalysisResult(
            session_id=session.id,
            elbow_angle=result["angles"]["elbow_angle"],
            knee_angle=result["angles"]["knee_angle"],
            shoulder_angle=result["angles"]["shoulder_angle"],
            release_frame=result["release_frame"],
        )
        db.add(analysis)

        for item in result["feedback"]:
            db.add(FeedbackItem(
                session_id=session.id,
                checkpoint_name=item["checkpoint"],
                angle_value=item["angle"],
                status=item["status"],
                tip=item["tip"],
            ))

        session.overall_score = result["overall_score"]
        session.annotated_video_url = result["annotated_video_url"]
        session.status = "done"

        db.commit()
    except Exception as e:
        session.status = "failed"
        session.error = str(e)
        db.commit()
        raise HTTPException(status_code=500, detail="Analysis failed")

    return AnalysisResponse(**result)