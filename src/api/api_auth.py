import secrets
from datetime import timedelta, datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.db import get_db
from src.db.models import PasswordResetToken
from src.repository.repo_users import UserRepository
from src.schemas import UserCreate, UserResponse, Token
from src.services.service_auth import (
    register_user,
    pwd_context,
    create_access_token,
    hash_password,
)
from src.services.services_email import send_email

router = APIRouter(prefix="/auth", tags=["auth"])
limiter = Limiter(key_func=get_remote_address)


@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup(user: UserCreate, db: AsyncSession = Depends(get_db)):
    repo = UserRepository(db)
    existing = await repo.get_by_email(user.email)
    if existing:
        raise HTTPException(status_code=409, detail="Email already exists")
    return await register_user(user, repo)


@router.post("/login", response_model=Token)
async def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: AsyncSession = Depends(get_db)
):
    repo = UserRepository(db)
    user = await repo.get_by_email(form_data.username)
    if not user or not pwd_context.verify(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = await create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/request-password-reset")
async def request_password_reset(user_email, db: AsyncSession = Depends(get_db)):
    user = await UserRepository(db).get_by_email(user_email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    token = secrets.token_urlsafe(32)
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=30)

    reset_token = PasswordResetToken(email=user.email, token=token, expires_at=expires_at)
    db.add(reset_token)
    await db.commit()

    reset_link = f"{router}/reset-password?token={token}"

    await send_email(
        to_email=user.email,
        subject="Password Reset Request",
        body=f"Click here to reset your password: {reset_link}"
    )

    return {"message": "Password reset link sent to email"}

@router.post("/reset-password")
async def reset_password(token: str, new_password: str, db: AsyncSession = Depends(get_db)):

    stmt = select(PasswordResetToken).where(PasswordResetToken.token == token)
    result = await db.execute(stmt)
    token_entry = result.scalars().first()

    if not token_entry or token_entry.expires_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    user = await UserRepository(db).get_by_email(token_entry.get("email"))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.password = hash_password(new_password)
    await db.delete(token_entry)
    await db.commit()

    return {"message": "Password has been reset successfully"}
