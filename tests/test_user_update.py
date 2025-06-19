import requests
import allure
from data.urls import BASE_URL
from data.texts import MSG_MUST_BE_AUTH

@allure.suite("User Update API")
class TestUserUpdateAPI:

    @allure.title("Обновление email пользователя с авторизацией")
    def test_update_user_email_authorized(self, register_user):
        url = f"{BASE_URL}/api/auth/user"
        headers = {"Authorization": register_user["access"]}
        new_email = "changed_" + register_user["email"]
        payload = {"email": new_email}
        resp = requests.patch(url, json=payload, headers=headers)
        assert resp.status_code == 200
        assert resp.json()["user"]["email"] == new_email

    @allure.title("Обновление имени пользователя с авторизацией")
    def test_update_user_name_authorized(self, register_user):
        url = f"{BASE_URL}/api/auth/user"
        headers = {"Authorization": register_user["access"]}
        new_name = "НовоеИмя"
        payload = {"name": new_name}
        resp = requests.patch(url, json=payload, headers=headers)
        assert resp.status_code == 200
        assert resp.json()["user"]["name"] == new_name

    @allure.title("Обновление пароля пользователя с авторизацией")
    def test_update_user_password_authorized(self, register_user):
        url = f"{BASE_URL}/api/auth/user"
        headers = {"Authorization": register_user["access"]}
        new_password = "NewSecretPass!"
        payload = {"password": new_password}
        resp = requests.patch(url, json=payload, headers=headers)
        assert resp.status_code == 200
        assert resp.json()["success"] is True

    @allure.title("Попытка изменить данные без авторизации")
    def test_update_user_unauthorized(self):
        resp = requests.patch(f"{BASE_URL}/api/auth/user", json={"name": "NoAuthName"})
        assert resp.status_code == 401
        assert resp.json()["message"] == MSG_MUST_BE_AUTH
