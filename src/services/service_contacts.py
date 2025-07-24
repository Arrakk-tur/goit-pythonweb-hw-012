from sqlalchemy.ext.asyncio import AsyncSession
from src.repository.repo_contacts import ContactRepository
from src.db.models import User
from src.schemas import ContactCreate, ContactUpdate

class ContactService:
    def __init__(self, db: AsyncSession):
        """
        Initialize the ContactService with a database session.

        :param db: Asynchronous database session.
        """
        self.repo = ContactRepository(db)

    async def create(self, body: ContactCreate, user:User):
        """
        Create a new contact for the authenticated user.

        :param body: Data for creating the contact.
        :param user: The authenticated user.
        :return: The newly created contact.
        """
        return await self.repo.create(body, user)

    async def get_all(self, user:User, skip: int, limit: int):
        """
        Retrieve all contacts belonging to the authenticated user.

        :param user: The authenticated user.
        :param skip: Number of records to skip.
        :param limit: Maximum number of records to return.
        :return: A list of contacts.
        """
        return await self.repo.get_all(user, skip, limit)

    async def get_by_id(self, contact_id: int, user:User):
        """
        Retrieve a specific contact by ID for the authenticated user.

        :param contact_id: The ID of the contact.
        :param user: The authenticated user.
        :return: Contact object if found, else None.
        """
        return await self.repo.get_by_id(contact_id, user)

    async def update(self, contact_id: int, body: ContactUpdate, user:User):
        """
        Update an existing contact by ID.

        :param contact_id: The ID of the contact to update.
        :param body: New data for the contact.
        :param user: The authenticated user.
        :return: The updated contact or None if not found.
        """
        return await self.repo.update(contact_id, body, user)

    async def delete(self, contact_id: int, user:User):
        """
        Delete a contact by ID.

        :param contact_id: The ID of the contact to delete.
        :param user: The authenticated user.
        :return: The deleted contact or None if not found.
        """
        return await self.repo.delete(contact_id, user)

    async def search(self, user:User, query: str):
        """
        Search contacts by first name, last name or email.

        :param user: The authenticated user.
        :param query: Search query string.
        :return: A list of matching contacts.
        """
        return await self.repo.search(user, query)

    async def upcoming_birthdays(self, user:User):
        """
        Retrieve contacts whose birthdays are in the next 7 days.

        :param user: The authenticated user.
        :return: A list of contacts with upcoming birthdays.
        """
        return await self.repo.upcoming_birthdays(user)