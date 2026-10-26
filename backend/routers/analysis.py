
import threading
import traceback
import uuid

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal, get_db
from models import ShotSession, AnalysisResult, FeedbackItem
from services import ml_pipeline
from services.deps import get_current_user
from pydantic import BaseModel

router = APIRouter()
_one_at_a_time = threading.Lock()
class AnalyzeRequest(BaseModel):
    session_id: str
    video_url: str

def save_results(db, session, result):
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


def run_analysis(session_id, video_url):
    db = SessionLocal()
    try:
        with _one_at_a_time:
            result = ml_pipeline.run(video_url, str(session_id))

        session = db.get(ShotSession, session_id)
        if session is None:
            return

        save_results(db, session, result)
        session.status = "done"
        session.error = None
        db.commit()

    except Exception:
        traceback.print_exc()
        db.rollback()

        session = db.get(ShotSession, session_id)
        if session is not None:
            session.status = "failed"
            session.error = (
                "We couldn't find a full shot in this video. "
                "Try filming from the side with your whole body in view."
            )
            db.commit()
    finally:
        db.close()


@router.post("/analyze", status_code=202)
def analyze(
    request: AnalyzeRequest,
    background: BackgroundTasks,
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

    session.status = "processing"
    session.error = None
    db.commit()

    background.add_task(run_analysis, session.id, session.video_url)

    return {
        "session_id": str(session.id),
        "status": "processing",
    }
