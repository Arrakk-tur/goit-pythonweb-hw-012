import datetime

import pytest
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import Contact, User
from src.repository.repo_contacts import ContactRepository
from src.schemas import ContactCreate, ContactUpdate

@pytest.fixture
def mock_session():
    return AsyncMock(spec=AsyncSession)

@pytest.fixture
def contact_repository(mock_session):
    return ContactRepository(mock_session)

@pytest.fixture
def user():
    return User(id=1, email="testuser@example.com")

@pytest.mark.asyncio
async def test_get_contacts(contact_repository, mock_session, user):
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = [
        Contact(id=1, first_name="Test", last_name="User", email="test@example.com", user=user)
    ]
    mock_session.execute = AsyncMock(return_value=mock_result)

    contacts = await contact_repository.get_all(skip=0, limit=10, user=user)

    assert len(contacts) == 1
    assert contacts[0].first_name == "Test"

@pytest.mark.asyncio
async def test_get_contact_by_id(contact_repository, mock_session, user):
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = Contact(
        id=1, first_name="Test", last_name="User", email="test@example.com", user=user
    )
    mock_session.execute = AsyncMock(return_value=mock_result)

    contact = await contact_repository.get_by_id(contact_id=1, user=user)

    assert contact is not None
    assert contact.first_name == "Test"

@pytest.mark.asyncio
async def test_create_contact(contact_repository, mock_session, user):
    contact_data = ContactCreate(
        first_name="Jane", last_name="Doe", email="jane@example.com", phone="1234567890", birthday=datetime.date.fromisoformat("1985-07-26")
    )
    result = await contact_repository.create(body=contact_data, user=user)

    assert isinstance(result, Contact)
    assert result.first_name == "Jane"
    assert result.email == "jane@example.com"

@pytest.mark.asyncio
async def test_update_contact(contact_repository, mock_session, user):
    contact_data = ContactUpdate(first_name="Updated", last_name="User", email="updated@example.com", phone="1234567890", birthday=datetime.date.fromisoformat("1985-07-26"))
    existing_contact = Contact(id=1, first_name="Old", last_name="User", email="old@example.com", user=user)

    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = existing_contact
    mock_session.execute = AsyncMock(return_value=mock_result)

    updated = await contact_repository.update(contact_id=1, body=contact_data, user=user)

    assert updated.first_name == "Updated"
    assert updated.email == "updated@example.com"
    mock_session.commit.assert_awaited_once()
    mock_session.refresh.assert_awaited_once_with(existing_contact)

@pytest.mark.asyncio
async def test_remove_contact(contact_repository, mock_session, user):
    existing_contact = Contact(id=1, first_name="ToDelete", last_name="User", email="del@example.com", user=user)

    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = existing_contact
    mock_session.execute = AsyncMock(return_value=mock_result)

    deleted = await contact_repository.delete(contact_id=1, user=user)

    assert deleted.first_name == "ToDelete"
    mock_session.delete.assert_awaited_once_with(existing_contact)
    mock_session.commit.assert_awaited_once()

@pytest.mark.asyncio
async def test_get_contact_by_id_not_found(contact_repository, mock_session, user):
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None
    mock_session.execute = AsyncMock(return_value=mock_result)

    contact = await contact_repository.get_by_id(contact_id=999, user=user)

    assert contact is None

@pytest.mark.asyncio
async def test_update_contact_not_found(contact_repository, mock_session, user):
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None
    mock_session.execute = AsyncMock(return_value=mock_result)

    result = await contact_repository.update(
        contact_id=999,
        body=ContactUpdate(first_name="X", last_name="Y", email="z@x.com", phone="1234567890", birthday=datetime.date.fromisoformat("1985-07-26")),
        user=user
    )

    assert result is None

@pytest.mark.asyncio
async def test_remove_contact_not_found(contact_repository, mock_session, user):
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None
    mock_session.execute = AsyncMock(return_value=mock_result)

    result = await contact_repository.delete(contact_id=999, user=user)

    assert result is None