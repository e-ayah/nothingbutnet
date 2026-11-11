import pytest

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


def test_signup_with_explicit_username(client):
    response = client.post('/auth/signup', json={
        'email': 'named@example.com', 'password': 'password123',
        'name': 'Named Player', 'username': 'Named_Player',
    })
    assert response.status_code == 200, response.text
    profile = client.get('/auth/me', headers={
        'Authorization': f"Bearer {response.json()['token']}",
    })
    assert profile.status_code == 200
    assert profile.json()['username'] == 'named_player'


def test_signup_generates_username_when_omitted(client):
    response = client.post('/auth/signup', json={
        'email': 'generated@example.com', 'password': 'password123', 'name': 'New Player',
    })
    assert response.status_code == 200, response.text
    profile = client.get('/auth/me', headers={
        'Authorization': f"Bearer {response.json()['token']}",
    })
    username = profile.json()['username']
    assert username.startswith('newplayer')
    assert username[-3:].isdigit()


def test_signup_rejects_duplicate_username(client):
    player = {'email': 'first@example.com', 'password': 'password123',
              'name': 'Player', 'username': 'same_player'}
    assert client.post('/auth/signup', json=player).status_code == 200
    response = client.post('/auth/signup', json={
        **player, 'email': 'second@example.com', 'username': 'SAME_PLAYER',
    })
    assert response.status_code == 400
    assert response.json()['detail'] == 'Username already taken'


@pytest.mark.parametrize('username', ['', 'ab', 'x' * 21, 'bad-name', 'has space'])
def test_signup_rejects_invalid_username(client, username):
    response = client.post('/auth/signup', json={
        'email': 'invalid@example.com', 'password': 'password123',
        'name': 'Player', 'username': username,
    })
    assert response.status_code == 400
    # A rejected username must not create an account that can log in.
    assert client.post('/auth/login', json={
        'email': 'invalid@example.com', 'password': 'password123',
    }).status_code == 401
