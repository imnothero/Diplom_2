import pytest
import requests

BASE_URL = "https://stellarburgers.nomoreparties.site"

class TestLoginAPI:

    def test_login_valid_user(self, register_user):
        """Логин под существующим пользователем"""
        payload = {"email": register_user["email"], "password": register_user["password"]}
        resp = requests.post(f"{BASE_URL}/api/auth/login", json=payload)
        assert resp.status_code == 200
        assert resp.json()["success"] is True
        assert "accessToken" in resp.json()

    @pytest.mark.parametrize("login,pwd", [
        ("fake@mail.ru", "TestPass123!"),
        ("", "TestPass123!"),
        ("user@notreal.com", ""),
        ("", ""),
    ])
    def test_login_invalid_credentials(self, login, pwd):
        """Логин с невалидными данными"""
        resp = requests.post(f"{BASE_URL}/api/auth/login", json={"email": login, "password": pwd})
        assert resp.status_code == 401
        assert resp.json()["message"] == "email or password are incorrect"
