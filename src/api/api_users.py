import os

from fastapi import APIRouter, Depends, UploadFile, File
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request
from src.db.db import get_db
from src.db.models import User
from src.repository.repo_users import UserRepository
from src.schemas import UserResponse
from src.services.service_auth import get_current_user

router = APIRouter(prefix="/user", tags=["user"])
limiter = Limiter(key_func=get_remote_address)

@router.get("/me", response_model=UserResponse)
@limiter.limit("5/minute")
async def get_me( request: Request, current_user: User = Depends(get_current_user)):
    return current_user

@router.post("/avatar")
async def upload_avatar_route(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    temp_dir = "temp"
    os.makedirs(temp_dir, exist_ok=True)

    temp_path = os.path.join(temp_dir, f"{current_user.id}_{file.filename}")
    with open(temp_path, "wb") as f:
        f.write(await file.read())

    from src.services.service_cloudinary import upload_avatar
    avatar_url = await upload_avatar(temp_path, public_id=f"user_avatars/{current_user.id}")
    os.remove(temp_path)

    updated_user = await UserRepository(db).update_avatar(current_user, avatar_url)
    return {"avatar_url": updated_user.avatar_url}