import pytest

from src.repository.repo_users import UserRepository
from src.services.service_auth import hash_password


@pytest.mark.asyncio
async def test_create_user(session):
    user_data = {
        "email": "tester_003@example.com",
        "password": "secret"
    }
    hashed = hash_password(user_data["password"])
    user = await UserRepository.create_user(session, user_data["email"], hashed)
    assert user.email == user_data["email"]


@pytest.mark.asyncio
async def test_get_user_by_email(session, test_user):
    user = await UserRepository.get_by_email(session, test_user.email)
    assert user.email == test_user.email
