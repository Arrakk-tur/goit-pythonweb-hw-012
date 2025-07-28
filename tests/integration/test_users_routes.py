import os
from fastapi import status
from unittest.mock import patch


def test_read_current_user(client, auth_headers):
    response = client.get("/api/user/me", headers=auth_headers)
    print(response.json())
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["email"].startswith("tester_user_static")

@patch("src.services.service_cloudinary.upload_avatar")
def test_update_avatar_user(mock_upload_file, client, auth_headers):
    # Мокаємо відповідь від сервісу завантаження файлів
    fake_url = "http://example.com/avatar.jpg"
    mock_upload_file.return_value = fake_url

    # Файл, який буде відправлено
    file_data = {"file": ("avatar.jpg", b"fake image content", "image/jpeg")}

    # Відправка PATCH-запиту
    response = client.patch("/api/users/avatar", headers=auth_headers, files=file_data)

    # Перевірка, що запит був успішним
    assert response.status_code == 200, response.text

    # Перевірка відповіді
    data = response.json()
    assert data["avatar_url"] == fake_url

    # Перевірка виклику функції upload_file
    mock_upload_file.assert_called_once()