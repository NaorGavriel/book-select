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
import pytest

from app.services.auth import (
    authenticate_user,
    create_refresh_token,
    refresh_access_token,
    create_new_user,
    InvalidRefreshToken,
    decode_token,
    hash_password,
    verify_password,
    create_access_token
)

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

def test_authenticate_user_success(mocker):
    """
    Should return user when email exists and password matches.
    """
    password = "1234"
    fake_user = mocker.Mock()
    fake_user.password_hash = hash_password(password)

    mocker.patch("app.services.auth.get_user", return_value=fake_user)
        
    result = authenticate_user(db=None, email="test@example.com", password=password)

    assert result == fake_user

def test_authenticate_user_wrong_password(mocker):
    """
    Should return False when password is incorrect.
    """
    fake_user = mocker.Mock()
    fake_user.password_hash = hash_password("correct")

    mocker.patch("app.services.auth.get_user", return_value=fake_user)

    result = authenticate_user(
        db=None,
        email="test@example.com",
        password="wrong"
    )

    assert result is False

def test_refresh_access_token_invalid_token():
    """
    Testing invalid refresh token
    """
    with pytest.raises(InvalidRefreshToken) as exc:
        refresh_access_token("invalid")

    assert "Invalid refresh token" in str(exc.value)

def test_refresh_access_token_missing():
    """
    Testing empty refresh token
    """
    with pytest.raises(InvalidRefreshToken) as exc:
        refresh_access_token("")

    assert "Missing refresh token" in str(exc.value)

def test_refresh_access_token_wrong_type():
    """
    Should raise when token is not a refresh token.
    """
    access_token = create_access_token({"sub": "test@example.com"})

    with pytest.raises(InvalidRefreshToken):
        refresh_access_token(access_token)

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

def test_create_refresh_token():
    """
    Should create a refresh token with correct payload.
    """
    data = {"sub": "test@example.com"}

    token = create_refresh_token(data)
    payload = decode_token(token)

    assert payload["sub"] == "test@example.com"
    assert payload["type"] == "refresh"

def test_refresh_access_token_success():
    """
    Should generate a new access token from a valid refresh token.
    """
    refresh_token = create_refresh_token({"sub": "test@example.com"})

    new_access = refresh_access_token(refresh_token)
    payload = decode_token(new_access)

    assert payload["sub"] == "test@example.com"
    assert payload["type"] == "access"

def test_create_new_user(mocker):
    """
    Should hash password and pass it to create_user.
    """
    mock_db = mocker.Mock()

    mock_create_user = mocker.patch("app.services.auth.create_user")

    create_new_user(mock_db, "test@example.com", "password123")

    args, kwargs = mock_create_user.call_args

    assert kwargs["email"] == "test@example.com"
    assert verify_password("password123", kwargs["hashed_password"])