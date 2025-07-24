from sqlalchemy.ext.asyncio import AsyncSession
from src.repository.repo_contacts import ContactRepository
from src.db.models import User
from src.schemas import ContactCreate, ContactUpdate

class ContactService:
    def __init__(self, db: AsyncSession):
        """
        Initialize the ContactService with a database session.

        Args:
            db: Asynchronous database session.
        """
        self.repo = ContactRepository(db)

    async def create(self, body: ContactCreate, user:User):
        """
        Create a new contact for the authenticated user.

        Args:
            body: Data for creating the contact.
            user: The authenticated user.
            Returns:
    The newly created contact.
        """
        return await self.repo.create(body, user)

    async def get_all(self, user:User, skip: int, limit: int):
        """
        Retrieve all contacts belonging to the authenticated user.

        Args:
            user: The authenticated user.
            skip: Number of records to skip.
            limit: Maximum number of records to return.

        Returns:
            A list of contacts.
        """
        return await self.repo.get_all(user, skip, limit)

    async def get_by_id(self, contact_id: int, user:User):
        """
        Retrieve a specific contact by ID for the authenticated user.

        Args:
            contact_id: The ID of the contact.
            user: The authenticated user.

        Returns:
            Contact object if found, else None.
        """
        return await self.repo.get_by_id(contact_id, user)

    async def update(self, contact_id: int, body: ContactUpdate, user:User):
        """
        Update an existing contact by ID.

        Args:
            contact_id: The ID of the contact to update.
            body: New data for the contact.
            user: The authenticated user.

        Returns:
            The updated contact or None if not found.
        """
        return await self.repo.update(contact_id, body, user)

    async def delete(self, contact_id: int, user:User):
        """
        Delete a contact by ID.

        Args:
            contact_id: The ID of the contact to delete.
            user: The authenticated user.

        Returns:
            The deleted contact or None if not found.
        """
        return await self.repo.delete(contact_id, user)

    async def search(self, user:User, query: str):
        """
        Search contacts by first name, last name or email.

        Args:
            user: The authenticated user.
            query: Search query string.

        Returns:
            A list of matching contacts.
        """
        return await self.repo.search(user, query)

    async def upcoming_birthdays(self, user:User):
        """
        Retrieve contacts whose birthdays are in the next 7 days.

        Args:
            user: The authenticated user.

        Returns:
            A list of contacts with upcoming birthdays.
        """
        return await self.repo.upcoming_birthdays(user)