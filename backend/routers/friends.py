from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import and_, or_
from sqlalchemy.orm import Session
from uuid import UUID
from database import get_db
from models import Friendship, User
from services.deps import get_current_user
from schemas.friends import FriendRequestIn, AcceptFriendResponse
 
router = APIRouter()
 
def friend_ids(db: Session, user_id):
    """Everyone with an ACCEPTED friendship with user_id (either direction). Sprint 8's leaderboard reuses this."""
    rows = db.query(Friendship).filter(Friendship.status == "accepted",
        or_(Friendship.requester_id == user_id, Friendship.addressee_id == user_id)).all()
    return [r.addressee_id if r.requester_id == user_id else r.requester_id for r in rows]
 
@router.post("/requests")
def send_request(body: FriendRequestIn, db: Session = Depends(get_db), user=Depends(get_current_user)):
    other = db.query(User).filter(User.username == body.username.lower()).first()
    if other is None:
        raise HTTPException(404, "No user with that username")
    if other.id == user.id:
        raise HTTPException(400, "You can't add yourself")
    exists = db.query(Friendship).filter(or_(
        and_(Friendship.requester_id == user.id, Friendship.addressee_id == other.id),
        and_(Friendship.requester_id == other.id, Friendship.addressee_id == user.id))).first()
    if exists:
        raise HTTPException(400, "You're already friends or have a pending request")
    f = Friendship(requester_id=user.id, addressee_id=other.id)
    db.add(f); db.commit(); db.refresh(f)
    return {"request_id": str(f.id), "status": "pending"}

@router.get("/requests")
def list_requests(db: Session = Depends(get_db), user=Depends(get_current_user)):
    incoming_rows = db.query(Friendship).filter(Friendship.addressee_id == user.id, Friendship.status == "pending").all()
    outgoing_rows = db.query(Friendship).filter(Friendship.requester_id == user.id, Friendship.status == "pending").all()
    incoming = []
    for r in incoming_rows:
        u = db.query(User).filter(User.id == r.requester_id).first()
        if u:
            incoming.append({"request_id": str(r.id), "from": {"user_id": str(u.id), "name": u.name, "username": u.username}})
    outgoing = []
    for r in outgoing_rows:
        u = db.query(User).filter(User.id == r.addressee_id).first()
        if u:
            outgoing.append({"request_id": str(r.id), "to": {"user_id": str(u.id), "name": u.name, "username": u.username}})
    return {"incoming": incoming, "outgoing": outgoing}

@router.post("/requests/{id}/accept", response_model=AcceptFriendResponse)
def accept_request(id: UUID, db: Session = Depends(get_db), user=Depends(get_current_user)):
    f = db.query(Friendship).filter(Friendship.id == id, Friendship.status == "pending").first()
    if not f:
        raise HTTPException(status_code=404, detail="Friend request not found")
    if f.addressee_id != user.id:
        raise HTTPException(status_code=403, detail="User is not the recipient of this request")
    f.status = "accepted"
    db.commit()
    requester = db.query(User).filter(User.id == f.requester_id).first()
    return {"friend": {"user_id": str(requester.id), "name": requester.name, "username": requester.username}}

@router.post("/requests/{id}/decline", status_code=status.HTTP_204_NO_CONTENT)
def decline_request(id: UUID, db: Session = Depends(get_db), user=Depends(get_current_user)):
    f = db.query(Friendship).filter(Friendship.id == id, Friendship.status == "pending").first()
    if not f:
        raise HTTPException(status_code=404, detail="Friend request not found")
    if f.addressee_id != user.id:
        raise HTTPException(status_code=403, detail="User is not the recipient of this request")
    db.delete(f)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.get("")
def list_friends(db: Session = Depends(get_db), user=Depends(get_current_user)):
    ids = friend_ids(db, user.id)
    users = db.query(User).filter(User.id.in_(ids)).all() if ids else []
    return [{"user_id": str(u.id), "name": u.name, "username": u.username} for u in users]

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_friend(user_id: UUID, db: Session = Depends(get_db), user=Depends(get_current_user)):
    f = db.query(Friendship).filter(
        or_(and_(Friendship.requester_id == user.id, Friendship.addressee_id == user_id), and_(Friendship.requester_id == user_id, Friendship.addressee_id == user.id))
    ).first()
    if not f:
        raise HTTPException(status_code=404, detail="Friend not found") 
    db.delete(f)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)