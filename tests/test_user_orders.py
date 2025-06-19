import pytest
import requests
import allure
from data.urls import BASE_URL
from data.texts import MSG_MUST_BE_AUTH

@allure.suite("User Orders API")
class TestUserOrdersAPI:

    @allure.title("Получение заказов пользователя (авторизован)")
    def test_get_orders_authorized(self, register_user, get_any_ingredient):
        # Сначала создаём заказ
        headers = {"Authorization": register_user["access"]}
        requests.post(f"{BASE_URL}/api/orders", json={"ingredients": [get_any_ingredient]}, headers=headers)
        # Затем получаем список заказов
        resp = requests.get(f"{BASE_URL}/api/orders", headers=headers)
        assert resp.status_code == 200
        assert resp.json()["success"] is True
        assert "orders" in resp.json()

    @allure.title("Получение заказов пользователя без авторизации")
    def test_get_orders_unauthorized(self):
        resp = requests.get(f"{BASE_URL}/api/orders")
        assert resp.status_code == 401
        assert resp.json()["message"] == MSG_MUST_BE_AUTH
