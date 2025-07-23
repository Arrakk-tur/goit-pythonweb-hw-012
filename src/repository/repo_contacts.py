from typing import List, Any, Coroutine, Sequence
from datetime import date, timedelta

from sqlalchemy import select, or_, func, Row, RowMapping
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import Contact, User
from src.schemas import ContactCreate, ContactUpdate

class ContactRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self, user:User, skip: int = 0, limit: int = 100) -> Sequence[Contact]:
        stmt = select(Contact).filter_by(user=user).offset(skip).limit(limit)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_by_id(self, contact_id: int, user:User) -> Contact | None:
        stmt = select(Contact).filter_by(id=contact_id, user=user)
        contact = await self.db.execute(stmt)
        return contact.scalar_one_or_none()

    async def create(self, body: ContactCreate, user:User) -> Contact:
        contact = Contact(**body.model_dump(exclude_unset=True), user=user)
        self.db.add(contact)
        await self.db.commit()
        await self.db.refresh(contact)
        return await self.get_by_id(contact.id, user)

    async def update(self, contact_id: int, body: ContactUpdate, user:User) -> Contact | None:
        contact = await self.get_by_id(contact_id, user)
        if contact:
            for field, value in body.model_dump().items():
                setattr(contact, field, value)
            await self.db.commit()
            await self.db.refresh(contact)
        return contact

    async def delete(self, contact_id: int, user:User) -> Contact | None:
        contact = await self.get_by_id(contact_id, user)
        if contact:
            await self.db.delete(contact)
            await self.db.commit()
        return contact

    async def search(self, user:User, query: str) -> Sequence[Contact]:
        stmt = select(Contact).where(
            Contact.user_id == user.id).where(
            or_(
                Contact.first_name.ilike(f"%{query}%"),
                Contact.last_name.ilike(f"%{query}%"),
                Contact.email.ilike(f"%{query}%")
            )
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def upcoming_birthdays(self, user:User) -> Sequence[Contact]:
        today = date.today()
        end = today + timedelta(days=7)
        stmt = select(Contact).where(
            Contact.user_id == user.id).where(
            func.date_part('doy', Contact.birthday).between(
                func.date_part('doy', today),
                func.date_part('doy', end)
            )
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()