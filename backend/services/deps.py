import uuid
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from database import get_db
from models import User
from services.security import decode_access_token
 
bearer = HTTPBearer(auto_error=False) # auto_error=False so WE return 401 (not 403)
 
def get_current_user(creds: HTTPAuthorizationCredentials | None = Depends(bearer),
        db: Session = Depends(get_db)) -> User:
    if creds is None:
        raise HTTPException(status_code=401, detail="Not logged in")
    try:
        user_id = decode_access_token(creds.credentials)
    except ValueError:
        raise HTTPException(status_code=401, detail="Your session expired. Log in again.")
    user = db.get(User, uuid.UUID(str(user_id)))
    if user is None:
        raise HTTPException(status_code=401, detail="Not logged in")
    return user