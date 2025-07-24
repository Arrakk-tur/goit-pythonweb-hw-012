from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.models import User

class UserRepository:
    def __init__(self, db: AsyncSession):
        """
        Initialize the user repository.

        :param db: Asynchronous database session.
        """
        self.db = db

    async def get_by_email(self, email: str) -> User | None:
        """
        Retrieve a user by email.

        :param email: Email address to search for.
        :return: User if found, else None.
        """
        stmt = select(User).where(User.email == email)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def create_user(self, email: str, hashed_password: str) -> User:
        """
        Create a new user with hashed password.

        :param email: Email address.
        :param hashed_password: Password hash.
        :return: The created User object.
        """
        user = User(email=email, hashed_password=hashed_password)
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def update_avatar(self, user: User, avatar_url: str) -> User:
        """
        Update the avatar URL of a user.

        :param user: The user to update.
        :param avatar_url: New avatar URL.
        :return: The updated User object.
        """
        user.avatar_url = avatar_url
        await self.db.commit()
        await self.db.refresh(user)
        return user