import os
from datetime import datetime, timedelta, timezone

from dotenv import load_dotenv
from jose import JWTError, jwt
from passlib.context import CryptContext

load_dotenv() #reads .env
SECRET_KEY = os.getenv("SECRET_KEY") #secret from .env
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#input: password (str)
#return: hashed password (str)
def hash_password(pw):
    return pwd_context.hash(pw)

#verifies if typed password (str) matches hashed password when hashed
#input: password (str), hashed password (str)
#return: bool -> true if match; false otherwise
def verify_password(pw, hashed):
    return pwd_context.verify(pw, hashed)

#signed token for user_id that expires in 'minutes' (default 1 week)
#input: user_id (int or str), minutes (int)
#return: str -> JWT token in "xxxxx.yyyyy.zzzzz" form
def create_access_token(user_id, minutes=60 * 24 * 7):
    expire = datetime.now(timezone.utc) + timedelta(minutes=minutes)
    payload = {"sub": str(user_id), "exp": expire} 
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

#makes sure that token is valid
#input: token (str)
#return: str -> user_id if token is valid
def decode_access_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) #checks signature + exp
    except JWTError as e:
        raise ValueError("Invalid or expired token") from e

    user_id = payload.get("sub")
    if user_id is None:
        raise ValueError("Token has no subject")
    return user_id