import os
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.engine import make_url
from sqlalchemy.orm import sessionmaker

# Add backend directory to Python's import path.
BACKEND_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND_DIR))

# Always connect to the separate test database.
TEST_DATABASE_URL = os.environ.get(
    "TEST_DATABASE_URL",
    "postgresql://localhost/nothingbutnet_test"
)

# Safety check: refuse to run against any other database.
if make_url(TEST_DATABASE_URL).database != "nothingbutnet_test":
    raise RuntimeError("Tests must use nothingbutnet_test!")

# database.py reads DATABASE_URL when it creates its engine.
os.environ["DATABASE_URL"] = TEST_DATABASE_URL

from models import Base
from database import get_db
from main import app

engine = create_engine(TEST_DATABASE_URL)
TestingSession = sessionmaker(bind=engine)


@pytest.fixture()
def client():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    def override_db():
        db = TestingSession()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_db

    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.clear()


@pytest.fixture()
def token(client):
    response = client.post(
        "/auth/signup",
        json={
            "email": "a@test.com",
            "password": "pass1234",
            "name": "A"
        }
    )

    assert response.status_code == 200, response.text
    return response.json()["token"]
@pytest.fixture()
def db_session(client):
    db = TestingSession()
    try:
        yield db
    finally:
        db.close()