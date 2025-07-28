from src.services.service_auth import hash_password, pwd_context, create_access_token

def test_password_hash():
    password = "supersecret"
    hashed = hash_password(password)
    assert pwd_context.verify(password, hashed)


def test_create_access_token():
    token = create_access_token(data={"sub": "user@example.com"})
    assert isinstance(token, str)