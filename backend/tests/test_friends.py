import time
from fastapi.testclient import TestClient
from main import app
from services.deps import get_db
from services.security import create_access_token
from models import User, Friendship

client = TestClient(app)

# Helper to fetch active DB session and instantiate a fresh test user
def create_test_player(username: str) -> User:
    db_gen = get_db()
    db = next(db_gen)
    try:
        timestamp = int(time.time() * 1000)
        user = User(
            email=f"{username}_{timestamp}@example.com",
            name=f"Player {username}",
            password_hash="fake_hash",
            username=username
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    finally:
        try:
            next(db_gen)
        except StopIteration:
            pass

# Helper to easily pass auth headers for a created user profile
def headers_for(user: User) -> dict:
    token = create_access_token(str(user.id))
    return {"Authorization": f"Bearer {token}"}

def test_requesting_yourself_fails():
    user = create_test_player("loner")
    headers = headers_for(user)
    
    response = client.post("/friends/requests", json={"username": "loner"}, headers=headers)
    assert response.status_code == 400

def test_requesting_unknown_username_fails():
    user = create_test_player("explorer")
    headers = headers_for(user)
    
    response = client.post("/friends/requests", json={"username": "nonexistent_ghost"}, headers=headers)
    assert response.status_code == 404

def test_send_friend_request_succeeds():
    sender = create_test_player("sender_a")
    receiver = create_test_player("receiver_b")
    
    response = client.post("/friends/requests", json={"username": "receiver_b"}, headers=headers_for(sender))
    assert response.status_code == 200
    assert response.json()["status"] == "pending"
    assert "request_id" in response.json()

def test_pending_request_appears_in_receiver_inbox():
    sender = create_test_player("sender_c")
    receiver = create_test_player("receiver_d")
    res_req = client.post("/friends/requests", json={"username": "receiver_d"}, headers=headers_for(sender))
    req_id = res_req.json()["request_id"]
    
    res_inbox = client.get("/friends/requests", headers=headers_for(receiver))
    assert res_inbox.status_code == 200
    
    incoming_list = res_inbox.json()["incoming"]
    assert len(incoming_list) == 1
    assert incoming_list[0]["request_id"] == req_id
    assert incoming_list[0]["from"]["username"] == "sender_c"

def test_accepting_request_returns_friend_details():
    sender = create_test_player("sender_e")
    receiver = create_test_player("receiver_f")
    res_req = client.post("/friends/requests", json={"username": "receiver_f"}, headers=headers_for(sender))
    req_id = res_req.json()["request_id"]
    
    res_accept = client.post(f"/friends/requests/{req_id}/accept", headers=headers_for(receiver))
    assert res_accept.status_code == 200
    assert res_accept.json()["friend"]["username"] == "sender_e"

def test_accepted_friends_list_populates_both_ways():
    sender = create_test_player("sender_g")
    receiver = create_test_player("receiver_h")
    res_req = client.post("/friends/requests", json={"username": "receiver_h"}, headers=headers_for(sender))
    req_id = res_req.json()["request_id"]
    client.post(f"/friends/requests/{req_id}/accept", headers=headers_for(receiver))
    
    res_list_sender = client.get("/friends", headers=headers_for(sender))
    assert "receiver_h" in [f["username"] for f in res_list_sender.json()]
    
    res_list_receiver = client.get("/friends", headers=headers_for(receiver))
    assert "sender_g" in [f["username"] for f in res_list_receiver.json()]

def test_removing_friend_clears_connection_both_ways():
    sender = create_test_player("sender_i")
    receiver = create_test_player("receiver_j")
    res_req = client.post("/friends/requests", json={"username": "receiver_j"}, headers=headers_for(sender))
    req_id = res_req.json()["request_id"]
    client.post(f"/friends/requests/{req_id}/accept", headers=headers_for(receiver))
    
    res_delete = client.delete(f"/friends/{receiver.id}", headers=headers_for(sender))
    assert res_delete.status_code == 204
    assert len(client.get("/friends", headers=headers_for(sender)).json()) == 0
    assert len(client.get("/friends", headers=headers_for(receiver)).json()) == 0