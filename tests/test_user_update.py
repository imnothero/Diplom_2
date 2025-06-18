import pytest
import requests

BASE_URL = "https://stellarburgers.nomoreparties.site"

class TestUserUpdateAPI:

    @pytest.mark.parametrize("field,value", [
        ("email", "changed_" + "".join("abc") + "@mail.ru"),
        ("name", "НовоеИмя"),
        ("password", "NewSecretPass!"),
    ])
    def test_update_user_authorized(self, register_user, field, value):
        """Обновление данных пользователя с авторизацией"""
        url = f"{BASE_URL}/api/auth/user"
        headers = {"Authorization": register_user["access"]}
        payload = {field: value}
        resp = requests.patch(url, json=payload, headers=headers)
        if field == "password":
            # Пароль нельзя проверить в ответе, проверяем success
            assert resp.status_code == 200
            assert resp.json()["success"] is True
        else:
            assert resp.status_code == 200
            assert resp.json()["user"][field] == value

    def test_update_user_unauthorized(self):
        """Попытка изменить данные без авторизации"""
        resp = requests.patch(f"{BASE_URL}/api/auth/user", json={"name": "NoAuthName"})
        assert resp.status_code == 401
        assert resp.json()["message"] == "You should be authorised"
