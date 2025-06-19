import pytest
import requests
import allure
from data.urls import BASE_URL
from data.texts import MSG_INVALID_CREDENTIALS

@allure.suite("Login API")
class TestLoginAPI:

    @allure.title("Логин под существующим пользователем")
    def test_login_valid_user(self, register_user):
        payload = {"email": register_user["email"], "password": register_user["password"]}
        resp = requests.post(f"{BASE_URL}/api/auth/login", json=payload)
        assert resp.status_code == 200
        assert resp.json()["success"] is True
        assert "accessToken" in resp.json()

    @allure.title("Логин с невалидными данными (параметризация)")
    @pytest.mark.parametrize("login,pwd", [
        ("fake@mail.ru", "TestPass123!"),
        ("", "TestPass123!"),
        ("user@notreal.com", ""),
        ("", ""),
    ])
    def test_login_invalid_credentials(self, login, pwd):
        resp = requests.post(f"{BASE_URL}/api/auth/login", json={"email": login, "password": pwd})
        assert resp.status_code == 401
        assert resp.json()["message"] == MSG_INVALID_CREDENTIALS
