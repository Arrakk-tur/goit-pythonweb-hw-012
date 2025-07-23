import cloudinary
import cloudinary.uploader
from src.conf.config import config

cloudinary.config(
    cloud_name=config.CLOUDINARY_CLOUD_NAME,
    api_key=config.CLOUDINARY_API_KEY,
    api_secret=config.CLOUDINARY_API_SECRET,
    secure=True
)

async def upload_avatar(file_path: str, public_id: str) -> str:
    result = cloudinary.uploader.upload(file_path, public_id=public_id, overwrite=True)
    return result.get("secure_url")