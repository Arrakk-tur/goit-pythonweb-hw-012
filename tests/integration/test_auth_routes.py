import pytest
from httpx import AsyncClient
from sqlalchemy import select

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
    assert response.status_code == 201
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
    assert response.status_code == 200, response.text
    data = response.json()
    assert "access_token" in data
    assert "token_type" in data