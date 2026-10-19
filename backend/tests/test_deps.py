from fastapi import FastAPI, Depends
from fastapi.testclient import TestClient
from services.deps import get_current_user, get_db
from services.security import create_access_token
from models import User
import time
 
app = FastAPI()
 
@app.get("/protected")
def protected(user=Depends(get_current_user)):
    return {"id": str(user.id)}
 
client = TestClient(app)
 
def test_no_header_is_401():
    assert client.get("/protected").status_code == 401
 
def test_garbage_token_is_401():
    r = client.get("/protected", headers={"Authorization": "Bearer not-a-token"})
    assert r.status_code == 401
 
# add: a valid token for a real user → 200 (create the user, then create_access_token(user.id))
def test_valid_token_is_200():
    db_gen = get_db()
    db = next(db_gen)
    try:
        unique_email = f"test_user_{int(time.time())}@example.com"

        test_user = User(
            email = unique_email,
            name = "Test User",
            password_hash = "fake_hash"
        )
        db.add(test_user)
        db.commit()
        db.refresh(test_user)

        token = create_access_token(str(test_user.id))
        headers = {"Authorization": f"Bearer {token}"}
        response = client.get("/protected", headers=headers)

        assert response.status_code == 200
        assert response.json() == {"id": str(test_user.id)}
    finally:
        try:
            next(db_gen)
        except StopIteration:
            pass