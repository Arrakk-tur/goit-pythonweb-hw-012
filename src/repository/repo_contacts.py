from typing import List, Any, Coroutine, Sequence
from datetime import date, timedelta

from sqlalchemy import select, or_, func, Row, RowMapping
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import Contact, User
from src.schemas import ContactCreate, ContactUpdate

class ContactRepository:
    def __init__(self, db: AsyncSession):
        """
        Initialize the contact repository.

        :param db: Asynchronous database session.
        """
        self.db = db

    async def get_all(self, user:User, skip: int = 0, limit: int = 100) -> Sequence[Contact]:
        """
        Retrieve all contacts for a given user.

        :param user: The user who owns the contacts.
        :param skip: Number of records to skip.
        :param limit: Maximum number of records to return.
        :return: A sequence of Contact objects.
        """
        stmt = select(Contact).filter_by(user=user).offset(skip).limit(limit)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_by_id(self, contact_id: int, user:User) -> Contact | None:
        """
        Retrieve a single contact by ID and user.

        :param contact_id: The ID of the contact.
        :param user: The owner user.
        :return: Contact if found, else None.
        """
        stmt = select(Contact).filter_by(id=contact_id, user=user)
        contact = await self.db.execute(stmt)
        return contact.scalar_one_or_none()

    async def create(self, body: ContactCreate, user:User) -> Contact:
        """
        Create a new contact and assign it to the user.

        :param body: Contact creation data.
        :param user: The user who creates the contact.
        :return: The created contact.
        """
        contact = Contact(**body.model_dump(exclude_unset=True), user=user)
        self.db.add(contact)
        await self.db.commit()
        await self.db.refresh(contact)
        return await self.get_by_id(contact.id, user)

    async def update(self, contact_id: int, body: ContactUpdate, user:User) -> Contact | None:
        """
        Update an existing contact with new data.

        :param contact_id: The ID of the contact to update.
        :param body: New contact data.
        :param user: The contact owner.
        :return: The updated contact or None if not found.
        """
        contact = await self.get_by_id(contact_id, user)
        if contact:
            for field, value in body.model_dump().items():
                setattr(contact, field, value)
            await self.db.commit()
            await self.db.refresh(contact)
        return contact

    async def delete(self, contact_id: int, user:User) -> Contact | None:
        """
        Delete a contact by ID.

        :param contact_id: The ID of the contact to delete.
        :param user: The contact owner.
        :return: The deleted contact or None if not found.
        """
        contact = await self.get_by_id(contact_id, user)
        if contact:
            await self.db.delete(contact)
            await self.db.commit()
        return contact

    async def search(self, user:User, query: str) -> Sequence[Contact]:
        """
        Search for contacts matching a query string.

        :param user: The owner of the contacts.
        :param query: Search string (name/email).
        :return: A sequence of matching contacts.
        """
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
        """
        Get contacts with birthdays in the next 7 days.

        :param user: The owner of the contacts.
        :return: A sequence of contacts with upcoming birthdays.
        """
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