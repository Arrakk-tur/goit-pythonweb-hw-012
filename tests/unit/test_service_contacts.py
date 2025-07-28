import pytest
from datetime import date, timedelta, timezone
from src.repository.repo_contacts import ContactRepository

@pytest.mark.asyncio
async def test_birthday_filter(session, test_user):
    today = date.today()
    upcoming = today + timedelta(days=5)
    await ContactRepository.create(session,
        {
            "first_name": "Bob",
            "last_name": "Lee",
            "email": "bob@example.com",
            "phone": "555-1234",
            "birthday": upcoming
        },
        user=test_user
    )
    results = await ContactRepository.upcoming_birthdays(session, test_user)
    assert any(c.email == "bob@example.com" for c in results)
