from app.services.auth import hash_password, verify_password, create_access_token, decode_token

def test_hash_and_verify_password():
    password = "my_secret"

    hashed = hash_password(password)

    assert hashed != password
    assert verify_password(password, hashed) is True
    assert verify_password("wrong", hashed) is False

def test_create_access_token():
    data = {"sub": "test@example.com"}

    token = create_access_token(data)

    payload = decode_token(token)

    assert payload["sub"] == "test@example.com"
    assert payload["type"] == "access"