import pytest

@pytest.mark.asyncio
async def test_create_contact(authorized_client):
    response = await authorized_client.post("/api/contacts", json={
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "phone": "123456789",
        "birthday": "1990-01-01"
    })
    assert response.status_code == 201
    assert response.json()["email"] == "john.doe@example.com"


@pytest.mark.asyncio
async def test_get_contacts(authorized_client):
    response = await authorized_client.get("/api/contacts")
    assert response.status_code == 200
    assert isinstance(response.json(), list)