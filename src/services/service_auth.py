import json

from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta, timezone
from typing import Optional

from src.conf.config import config
from src.schemas import UserCreate
from src.repository.repo_users import UserRepository
from src.db.db import get_db
from src.db.models import User, UserRole
from src.services.service_cache import redis_client

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

async def register_user(user: UserCreate, repo: UserRepository) -> User:
    """
    Register a new user by hashing their password and saving to the database.

    :param user: User registration data.
    :param repo: UserRepository instance.
    :return: The created user.
    """
    hashed_password = hash_password(user.password)
    # hashed_password = pwd_context.hash(user.password)
    return await repo.create_user(user.email, hashed_password)


async def create_access_token(data: dict, expires_delta: Optional[int] = None):
    """
    Create a JWT access token.

    :param data: Data to encode into the token.
    :param expires_delta: Optional expiration time in seconds.
    :return: Encoded JWT token string.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + timedelta(seconds=expires_delta)
    else:
        expire = datetime.now(timezone.utc) + timedelta(seconds=config.JWT_EXPIRATION_SECONDS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, config.JWT_SECRET, algorithm=config.JWT_ALGORITHM
    )
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)) -> User:
    """
    Retrieve the currently authenticated user from the token.

    :param token: JWT token string.
    :param db: Async database session.
    :return: The authenticated user.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(token, config.JWT_SECRET, algorithms=[config.JWT_ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        # Спроба дістати з Redis
        cached_user = await redis_client.get(f"user:{email}")
        if cached_user:
            user_data = json.loads(cached_user)
            return User(**user_data)

        user = await UserRepository(db).get_by_email(email)
        if user is None:
            raise credentials_exception

        user_dict = {
            "id": user.id,
            "email": user.email,
            "hashed_password": user.hashed_password,
            "avatar_url": user.avatar_url,
            "role": user.role.value,
            "is_active": user.is_active,
            "is_verified": user.is_verified,
        }

        await redis_client.set(f"user:{email}", json.dumps(user_dict), ex=600)

        return user
    except JWTError:
        raise credentials_exception

def hash_password(password: str) -> str:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.hash(password)


def ensure_is_admin(user: User):
    """
    Ensure User is Admin.

    :param user: User data.
    """

    if user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
