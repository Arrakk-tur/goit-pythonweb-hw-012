import pytest
from sqlalchemy import select
from fastapi import status

from src.db.models import User
from tests.conftest import TestingSessionLocal
from tests.test_utils import test_user
from tests.conftest import tester_user_static

current_test_user = test_user()


def test_register_user(client):
    response = client.post("/api/auth/signup", json={
        "email": current_test_user["email"],
        "password": current_test_user["password"]
    })
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["email"] == current_test_user["email"]

@pytest.mark.asyncio
async def test_login(client):
    async with TestingSessionLocal() as session:
        current_user = await session.execute(select(User).where(User.email == tester_user_static["email"]))
        current_user = current_user.scalar_one_or_none()
        if current_user:
            current_user.confirmed = True
            await session.commit()

    response = client.post("api/auth/login",
                           data={"username": tester_user_static["email"], "password": tester_user_static["password"]})
    assert response.status_code == status.HTTP_200_OK, response.text
    data = response.json()
    assert "access_token" in data
    assert "token_type" in data


def test_repeat_signup(client):
    response = client.post("/api/auth/signup", json={
        "email": current_test_user["email"],
        "password": current_test_user["password"]
    })
    assert response.status_code == status.HTTP_409_CONFLICT


@pytest.mark.parametrize("email,password,status_code", [
    ("tester_user_999@example.com", "wrongpass", status.HTTP_401_UNAUTHORIZED),  # wrong password
    ("wrong_user@example.com", "testpass123", status.HTTP_401_UNAUTHORIZED),     # wrong username/email
    ("", "", status.HTTP_401_UNAUTHORIZED),                               # validation error
])
def test_login_failures(client, email, password, status_code):
    response = client.post("/api/auth/login", data={
        "username": email,
        "password": password
    }, headers={"Content-Type": "application/x-www-form-urlencoded"})
    assert response.status_code == status_code
