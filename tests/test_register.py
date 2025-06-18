import pytest
import requests

BASE_URL = "https://stellarburgers.nomoreparties.site"

class TestRegistrationAPI:

    def test_create_unique_user(self, new_user):
        """Создание уникального пользователя"""
        resp = requests.post(f"{BASE_URL}/api/auth/register", json=new_user)
        assert resp.status_code == 200
        assert resp.json().get("success") is True
        # Чистим пользователя
        access_token = resp.json().get("accessToken")
        if access_token:
            requests.delete(f"{BASE_URL}/api/auth/user", headers={"Authorization": access_token})

    def test_create_existing_user(self, register_user):
        """Попытка создать уже существующего пользователя"""
        payload = {"email": register_user["email"], "password": register_user["password"], "name": "OtherName"}
        resp = requests.post(f"{BASE_URL}/api/auth/register", json=payload)
        assert resp.status_code == 403
        assert resp.json()["message"] == "User already exists"

    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_create_user_missing_field(self, new_user, missing_field):
        """Создание пользователя без одного из обязательных полей"""
        user_data = new_user.copy()
        user_data.pop(missing_field)
        resp = requests.post(f"{BASE_URL}/api/auth/register", json=user_data)
        assert resp.status_code == 403
        assert resp.json()["message"] == "Email, password and name are required fields"
