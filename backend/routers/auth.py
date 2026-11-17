import re
import random
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from database import get_db
from models import User
from schemas.auth import SignupRequest, LoginRequest, AuthResponse
from services.security import hash_password, verify_password, create_access_token
from services.deps import get_current_user
 
router = APIRouter()
 
@router.post("/signup", response_model=AuthResponse)
def signup(body: SignupRequest, db: Session = Depends(get_db)):
    username = body.username
    email = body.email.lower()
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    if username is not None:
        username_final = username.lower()
        if not (3 <= len(username_final) <= 20):
            raise HTTPException(status_code=400, detail="Username must be between 3 and 20 characters")
        if not re.match(r"^[a-z0-9_]+$", username_final):
            raise HTTPException(status_code=400, detail="Username must contain only lowercase letters, numbers, or underscores")
        if db.query(User).filter(User.username == username_final).first():
            raise HTTPException(status_code=400, detail="Username already taken")
    else:
        clean_name = "".join(c for c in body.name.lower() if c.isalnum() or c == "_")
        if clean_name:
            base = clean_name[:17]
        else:
            base = "player"
        while True:
            digits = random.randint(100, 999)
            candidate = f"{base}{digits}"
            if not db.query(User).filter(User.username == candidate).first():
                username_final = candidate
                break
    
    user = User(email=email, name=body.name, password_hash=hash_password(body.password), username=username_final)
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
        "email": user.email,
        "username": user.username
    }

@router.patch("/me")
def patch_me(username: str = Body(..., embed=True), db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    username_final = username.lower()
    if not (3 <= len(username_final) <= 20):
        raise HTTPException(status_code=400, detail="Username must be between 3 and 20 characters")
    if not re.match(r"^[a-z0-9_]+$", username_final):
        raise HTTPException(status_code=400, detail="Username must contain only lowercase letters, numbers, or underscores")
    
    existing = db.query(User).filter(User.username == username_final).first()
    if existing and existing.id != user.id:
        raise HTTPException(status_code=400, detail="Username already taken")
        
    setattr(user, "username", username_final)
    db.commit()
    db.refresh(user)
    return {
        "id": str(user.id),
        "name": user.name,
        "email": user.email,
        "username": user.username
    }
