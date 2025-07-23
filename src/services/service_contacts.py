from sqlalchemy.ext.asyncio import AsyncSession
from src.repository.repo_contacts import ContactRepository
from src.db.models import User
from src.schemas import ContactCreate, ContactUpdate

class ContactService:
    def __init__(self, db: AsyncSession):
        self.repo = ContactRepository(db)

    async def create(self, body: ContactCreate, user:User):
        return await self.repo.create(body, user)

    async def get_all(self, user:User, skip: int, limit: int):
        return await self.repo.get_all(user, skip, limit)

    async def get_by_id(self, contact_id: int, user:User):
        return await self.repo.get_by_id(contact_id, user)

    async def update(self, contact_id: int, body: ContactUpdate, user:User):
        return await self.repo.update(contact_id, body, user)

    async def delete(self, contact_id: int, user:User):
        return await self.repo.delete(contact_id, user)

    async def search(self, user:User, query: str):
        return await self.repo.search(user, query)

    async def upcoming_birthdays(self, user:User):
        return await self.repo.upcoming_birthdays(user)