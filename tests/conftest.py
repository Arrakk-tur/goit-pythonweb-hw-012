from random import randint
import asyncio

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.pool import StaticPool

from main import app
from src.db.models import Base, User
from src.db.db import get_db
from src.services.service_auth import create_access_token, hash_password

# Тестова БД SQLite
SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

# Асинхронний движок з StaticPool
engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

# Фабрика сесій
TestingSessionLocal = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    bind=engine,
)

# Тестовий користувач
rand_num = randint(100, 1000)
test_user = {
    "email": f"tester_user_{rand_num}@example.com",
    "hashed_password": hash_password("testpass123"),
}

# Створення таблиць і тестового користувача
@pytest.fixture(scope="module", autouse=True)
def init_models_wrap():
    async def init_models():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

        async with TestingSessionLocal() as session:
            user = User(
                email=test_user["email"],
                hashed_password=test_user["hashed_password"],
            )
            session.add(user)
            await session.commit()

    asyncio.run(init_models())

# Замінюємо залежність get_db на тестову
@pytest.fixture(scope="module")
def client():
    async def override_get_db():
        async with TestingSessionLocal() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

# Отримання токена для авторизованих запитів
@pytest_asyncio.fixture()
async def auth_headers():
    token = await create_access_token(data={"sub": test_user["username"]})
    return {"Authorization": f"Bearer {token}"}