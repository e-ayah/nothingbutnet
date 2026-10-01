import os
os.environ.setdefault("SECRET_KEY", "test-secret-key") #fallback key if no .env

import pytest

from services.security import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)

#right password verifies
def test_hash_then_verify():
    hashed = hash_password("hunter2")
    assert hashed != "hunter2" #actually scrambled
    assert verify_password("hunter2", hashed)

#wrong password doesn't
def test_wrong_password():
    hashed = hash_password("hunter2")
    assert not verify_password("wrong", hashed)

#token decodes back to same user id
def test_token_round_trip():
    token = create_access_token(42)
    assert decode_access_token(token) == "42"

#expired token fails
def test_expired_token_fails():
    token = create_access_token(42, minutes=-1) #expired 1 min ago
    with pytest.raises(ValueError):
        decode_access_token(token)

#edited token fails
def test_edited_token_fails():
    header, payload, sig = create_access_token(42).split(".")
    new_first = "f" if payload[0] != "f" else "g" #change 1 char of payload
    tampered = f"{header}.{new_first}{payload[1:]}.{sig}"
    with pytest.raises(ValueError):
        decode_access_token(tampered)