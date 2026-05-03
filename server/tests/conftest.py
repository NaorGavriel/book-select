import pytest
from app.services.auth import hash_password, create_refresh_token

@pytest.fixture
def fake_user(mocker):
    user = mocker.Mock()
    user.password_hash = hash_password("correct")
    user.email = "test@example.com"
    user.id = 1
    return user

@pytest.fixture
def mock_db(mocker):
    return mocker.Mock()

@pytest.fixture
def valid_refresh_token():
    return create_refresh_token({"sub": "test@example.com"})