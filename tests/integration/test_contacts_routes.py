import pytest
from fastapi import status

def test_create_contact(client, auth_headers):
    response = client.post("/api/contacts/", json={
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "phone": "1234567890",
        "birthday": "1990-01-01"
    }, headers=auth_headers)
    assert response.status_code == status.HTTP_201_CREATED
    assert "id" in response.json()
    global contact_id
    contact_id = response.json()["id"]


def test_get_contacts(client, auth_headers):
    response = client.get("/api/contacts", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)

from fastapi import status


def test_get_contact_by_id(client, auth_headers):
    response = client.get(f"/api/contacts/{contact_id}", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["email"] == "john.doe@example.com"


def test_get_contact_not_found(client, auth_headers):
    response = client.get("/api/contacts/9999", headers=auth_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_update_contact(client, auth_headers):
    response = client.put(f"/api/contacts/{contact_id}", json={
        "first_name": "John",
        "last_name": "Smith",
        "email": "john.smith@example.com",
        "phone": "9876543210",
        "birthday": "1990-01-01"
    }, headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["email"] == "john.smith@example.com"


def test_update_contact_not_found(client, auth_headers):
    response = client.put("/api/contacts/9999", json={
        "first_name": "Ghost",
        "last_name": "Contact",
        "email": "ghost@example.com",
        "phone": "0000000000",
        "birthday": "2000-01-01"
    }, headers=auth_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_contact(client, auth_headers):
    response = client.delete(f"/api/contacts/{contact_id}", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK


def test_repeat_delete_contact(client, auth_headers):
    response = client.delete(f"/api/contacts/{contact_id}", headers=auth_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND
