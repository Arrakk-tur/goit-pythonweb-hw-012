import pytest

@pytest.mark.asyncio
async def test_read_current_user(authorized_client):
    response = await authorized_client.get("/api/user/me")
    assert response.status_code == 200
    assert response.json()["email"].startswith("tester_user_static")
