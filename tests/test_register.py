import pytest
import requests
import allure
from data.urls import BASE_URL
from data.texts import MSG_USER_EXISTS, MSG_MISSING_FIELD

@allure.suite("Registration API")
class TestRegistrationAPI:

    @allure.title("Создание уникального пользователя")
    def test_create_unique_user(self, new_user):
        resp = requests.post(f"{BASE_URL}/api/auth/register", json=new_user)
        assert resp.status_code == 200
        assert resp.json().get("success") is True
        access_token = resp.json().get("accessToken")
        if access_token:
            requests.delete(f"{BASE_URL}/api/auth/user", headers={"Authorization": access_token})

    @allure.title("Попытка создать уже существующего пользователя")
    def test_create_existing_user(self, register_user):
        payload = {"email": register_user["email"], "password": register_user["password"], "name": "OtherName"}
        resp = requests.post(f"{BASE_URL}/api/auth/register", json=payload)
        assert resp.status_code == 403
        assert resp.json()["message"] == MSG_USER_EXISTS

    @allure.title("Создание пользователя без одного из обязательных полей (параметризация)")
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_create_user_missing_field(self, new_user, missing_field):
        user_data = new_user.copy()
        user_data.pop(missing_field)
        resp = requests.post(f"{BASE_URL}/api/auth/register", json=user_data)
        assert resp.status_code == 403
        assert resp.json()["message"] == MSG_MISSING_FIELD
