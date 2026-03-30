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


# =========================
# Passwords
# =========================

def test_hash_and_verify_password():
    """
    Ensure passwords are hashed and verified correctly.
    """
    password = "my_secret"

    hashed = hash_password(password)

    assert hashed != password
    assert verify_password(password, hashed)
    assert not verify_password("wrong", hashed)


# =========================
# authenticate_user
# =========================

def test_authenticate_user_success(mocker, fake_user, mock_db):
    """
    Should return user when email exists and password matches.
    """
    # fake_user already has password "correct" from fixture
    mocker.patch("app.services.auth.get_user", return_value=fake_user)

    result = authenticate_user(
        db=mock_db,
        email="test@example.com",
        password="correct"
    )

    assert result == fake_user


def test_authenticate_user_wrong_password(mocker, fake_user, mock_db):
    """
    Should return False when password is incorrect.
    """
    mocker.patch("app.services.auth.get_user", return_value=fake_user)

    result = authenticate_user(
        db=mock_db,
        email="test@example.com",
        password="wrong"
    )

    assert result is False


# =========================
# Refresh token errors
# =========================

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

    with pytest.raises(InvalidRefreshToken) as exc:
        refresh_access_token(access_token)

    assert "Invalid token type" in str(exc.value)


# =========================
# Token creation
# =========================

def test_create_access_token():
    """
    Ensure access token is created with correct payload.
    """
    token = create_access_token({"sub": "test@example.com"})
    payload = decode_token(token)

    assert payload["sub"] == "test@example.com"
    assert payload["type"] == "access"


def test_create_refresh_token():
    """
    Should create a refresh token with correct payload.
    """
    token = create_refresh_token({"sub": "test@example.com"})
    payload = decode_token(token)

    assert payload["sub"] == "test@example.com"
    assert payload["type"] == "refresh"


# =========================
# Refresh token success
# =========================

def test_refresh_access_token_success(valid_refresh_token):
    """
    Should generate a new access token from a valid refresh token.
    """
    new_access = refresh_access_token(valid_refresh_token)
    payload = decode_token(new_access)

    assert payload["sub"] == "test@example.com"
    assert payload["type"] == "access"


# =========================
# create_new_user
# =========================

def test_create_new_user(mocker, mock_db):
    """
    Should hash password and pass it to create_user.
    """
    mock_create_user = mocker.patch("app.services.auth.create_user")

    create_new_user(mock_db, "test@example.com", "password123")

    args, kwargs = mock_create_user.call_args

    assert kwargs["email"] == "test@example.com"
    assert verify_password("password123", kwargs["hashed_password"])