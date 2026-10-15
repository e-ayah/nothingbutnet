from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import User
from schemas.auth import SignupRequest, LoginRequest, AuthResponse
from services.security import hash_password, verify_password, create_access_token
from services.deps import get_current_user
 
router = APIRouter()
 
@router.post("/signup", response_model=AuthResponse)
def signup(body: SignupRequest, db: Session = Depends(get_db)):
    email = body.email.lower()
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    user = User(email=email, name=body.name, password_hash=hash_password(body.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return AuthResponse(user_id=str(user.id), token=create_access_token(user.id))
 
@router.post("/login", response_model=AuthResponse)
def login(body: LoginRequest, db: Session = Depends(get_db)):
    email = body.email.lower()
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(body.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Wrong email or password")
    return AuthResponse(user_id=str(user.id), token=create_access_token(user.id))

@router.get("/me")
def get_me(user: User = Depends(get_current_user)):
    return {
        "id": str(user.id),
        "name": user.name,
        "email": user.email
    }