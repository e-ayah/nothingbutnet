from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from database import get_db
from models import ShotSession, User
from routers.friends import friend_ids
from services.deps import get_current_user
 
router = APIRouter()
MIN_SHOTS = 5
 
@router.get("")          # registered with prefix /leaderboard
def leaderboard(period: str = Query("week", pattern="^(week|all)$"),
                db: Session = Depends(get_db), user=Depends(get_current_user)):
    people = [user.id] + friend_ids(db, user.id)
    q = (db.query(ShotSession,)
           .filter(ShotSession.user_id.in_(people), ShotSession.made.isnot(None)))
    if period == "week":
        q = q.filter(ShotSession.created_at >= datetime.utcnow() - timedelta(days=7))
    stats = {pid: {"made": 0, "attempts": 0, "scores": []} for pid in people}
    for s in q.all():
        st = stats[s.user_id]
        st["attempts"] += 1
        st["made"] += 1 if s.made is True else 0
        if s.overall_score is not None:
            st["scores"].append(s.overall_score)
    names = {u.id: u.name for u in db.query(User).filter(User.id.in_(people))}
    rows = [{"user_id": str(pid), "name": names.get(pid, ""), "made": st["made"], "attempts": st["attempts"],
             "make_pct": round(100 * st["made"] / st["attempts"]) if st["attempts"] else 0,
             "avg_score": round(sum(st["scores"]) / len(st["scores"])) if st["scores"] else None,
             "is_me": pid == user.id} for pid, st in stats.items()]
    ranked = sorted([r for r in rows if r["attempts"] >= MIN_SHOTS],
                    key=lambda r: (-r["make_pct"], -r["attempts"]))
    for i, r in enumerate(ranked, start=1):
        r["rank"] = i
    unranked = [dict(r, rank=None) for r in rows if r["attempts"] < MIN_SHOTS]
    return ranked + unranked