
from collections import Counter
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import ShotSession, FeedbackItem
from services.deps import get_current_user
 
router = APIRouter()
LABELS = {"elbow_alignment": "Elbow", "knee_bend": "Knee bend", "shoulder_position": "Shoulder"}
 
@router.get("/recurring")          # registered with prefix /insights
def recurring(db: Session = Depends(get_db), user=Depends(get_current_user)):
    recent = (db.query(ShotSession)
                .filter(ShotSession.user_id == user.id, ShotSession.status == "done")
                .order_by(ShotSession.created_at.desc()).limit(5).all())
    if len(recent) < 3:
        return []
    ids = [s.id for s in recent]
    rows = db.query(FeedbackItem).filter(FeedbackItem.session_id.in_(ids)).all()
    counts = Counter(r.checkpoint_name for r in rows if r.status == "needs_work")  # FeedbackItem stores it as checkpoint_name
    out = []
    for checkpoint, n in counts.most_common():
        if n >= 3:
            latest = next(r for s in recent for r in rows
                          if r.session_id == s.id and r.checkpoint_name == checkpoint)
            out.append({"checkpoint": checkpoint, "label": LABELS.get(checkpoint, checkpoint),
                        "count": n, "out_of": len(recent), "latest_tip": latest.tip})
    return out
# Swap in the real model names for sessions and feedback rows (models.py).

