
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import ShotSession, AnalysisResult
from services.deps import get_current_user

router = APIRouter()

KEYS = ("elbow_angle", "knee_angle", "shoulder_angle")


def load(db, session_id, user):
    row = (
        db.query(ShotSession, AnalysisResult)
        .join(
            AnalysisResult,
            AnalysisResult.session_id == ShotSession.id
        )
        .filter(
            ShotSession.id == session_id,
            ShotSession.user_id == user.id,
            ShotSession.status == "done"
        )
        .first()
    )

    if row is None:
        raise HTTPException(404, "Session not found")

    s, r = row

    return {
        "session_id": str(s.id),
        "created_at": s.created_at.isoformat(),
        "video_url": s.video_url,
        "annotated_video_url": r.annotated_video_url,
        "angles": {
            k: getattr(r, k) for k in KEYS
        },
        "score": r.overall_score
    }


@router.get("/compare")
def compare(
    a: str,
    b: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    sa = load(db, a, user)
    sb = load(db, b, user)

    changes = {}

    for k in KEYS:
        angle_a = sa["angles"][k]
        angle_b = sb["angles"][k]

        if angle_a is None or angle_b is None:
            changes[k] = None
        else:
            changes[k] = round(angle_b - angle_a, 1)

    changes["score"] = round(
        sb["score"] - sa["score"], 1
    )

    return {
        "a": sa,
        "b": sb,
        "changes": changes
    }
