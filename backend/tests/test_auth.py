
def test_signup_success(client):
    response = client.post(
        "/auth/signup",
        json={
            "email": "test@example.com",
            "password": "password123",
            "name": "Test User"
        }
    )

    assert response.status_code == 200
    assert "token" in response.json()
    assert "user_id" in response.json()


def test_duplicate_email(client):
    user = {
        "email": "test@example.com",
        "password": "password123",
        "name": "Test User"
    }

    client.post("/auth/signup", json=user)
    response = client.post("/auth/signup", json=user)

    assert response.status_code == 400


def test_login_success(client):
    client.post(
        "/auth/signup",
        json={
            "email": "test@example.com",
            "password": "password123",
            "name": "Test User"
        }
    )

    response = client.post(
        "/auth/login",
        json={
            "email": "test@example.com",
            "password": "password123"
        }
    )

    assert response.status_code == 200
    assert "token" in response.json()


def test_login_wrong_password(client):
    client.post(
        "/auth/signup",
        json={
            "email": "test@example.com",
            "password": "password123",
            "name": "Test User"
        }
    )

    response = client.post(
        "/auth/login",
        json={
            "email": "test@example.com",
            "password": "wrongpassword"
        }
    )

    assert response.status_code == 401


def test_auth_me_with_token(client, token):
    response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.json()["email"] == "a@test.com"
    assert response.json()["name"] == "A"


def test_auth_me_without_token(client):
    response = client.get("/auth/me")

    assert response.status_code == 401
