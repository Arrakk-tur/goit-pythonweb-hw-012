import os
from dotenv import load_dotenv

load_dotenv()

class Config:

    # DB
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")

    DB_URL = (
        f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    # alembic
    SYNC_DB_URL = (
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    # JWT
    JWT_SECRET = os.getenv("JWT_SECRET")
    JWT_ALGORITHM = "HS256"
    JWT_EXPIRATION_SECONDS = 3600

    # CLOUDINARY
    CLOUDINARY_CLOUD_NAME=os.getenv("CLOUDINARY_CLOUD_NAME")
    CLOUDINARY_API_KEY=os.getenv("CLOUDINARY_API_KEY")
    CLOUDINARY_API_SECRET=os.getenv("CLOUDINARY_API_SECRET")

    # REDIS
    redis_host: str = "localhost"
    redis_port: int = 6379

    # SMTP

    SMTP_HOST=os.getenv("SMTP_HOST")
    SMTP_PORT=os.getenv("SMTP_PORT")
    SMTP_USER=os.getenv("SMTP_USER")
    SMTP_PASSWORD=os.getenv("SMTP_PASSWORD")
    FRONTEND_URL=os.getenv("FRONTEND_URL")

config = Config()
