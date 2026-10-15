from pydantic import BaseModel

# everything per api contract

class SignupRequest(BaseModel):
    email: str
    password: str
    name: str

class LoginRequest(BaseModel):
    email: str
    password: str

class AuthResponse(BaseModel):
    user_id: str # maybe should be int instead?
    token: str