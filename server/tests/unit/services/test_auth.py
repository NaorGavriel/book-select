"""
Unit tests for authentication utilities.

Covers:
- Password hashing and verification
- JWT access token creation and decoding

These tests are pure unit tests:
- No database interaction
- No external services
- No FastAPI dependencies

Assumptions:
- Environment variables are available
"""
from app.services.auth import hash_password, verify_password, create_access_token, decode_token

def test_hash_and_verify_password():
    """
    Ensure passwords are hashed and verified correctly.

    - Hash should not equal raw password
    - Correct password should validate
    - Incorrect password should fail
    """
    password = "my_secret"

    hashed = hash_password(password)

    assert hashed != password
    assert verify_password(password, hashed) is True
    assert verify_password("wrong", hashed) is False

def test_create_access_token():
    """
    Ensure access token is created with correct payload.

    - Token should include 'sub' (subject)
    - Token type should be 'access'
    - Decoding should return original data
    """
    data = {"sub": "test@example.com"}

    token = create_access_token(data)

    payload = decode_token(token)

    assert payload["sub"] == "test@example.com"
    assert payload["type"] == "access"