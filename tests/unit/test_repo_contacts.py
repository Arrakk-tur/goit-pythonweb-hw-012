import pytest
from src.repository.repo_contacts import ContactRepository
from src.schemas import ContactCreate

@pytest.mark.asyncio
async def test_create_contact(session, test_user):
    contact_data = ContactCreate(
        first_name="Alice",
        last_name="Smith",
        email="alice@example.com",
        phone="987654321",
        birthday="1985-05-10"
    )
    contact = await ContactRepository.create(session, contact_data, test_user)
    assert contact.email == contact_data.email
