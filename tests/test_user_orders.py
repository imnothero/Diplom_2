import pytest
import requests

BASE_URL = "https://stellarburgers.nomoreparties.site"

class TestUserOrdersAPI:

    def test_get_orders_authorized(self, register_user, get_any_ingredient):
        """Получение заказов пользователя (авторизован)"""
        # Сначала создаём заказ
        headers = {"Authorization": register_user["access"]}
        requests.post(f"{BASE_URL}/api/orders", json={"ingredients": [get_any_ingredient]}, headers=headers)
        # Затем получаем список заказов
        resp = requests.get(f"{BASE_URL}/api/orders", headers=headers)
        assert resp.status_code == 200
        assert resp.json()["success"] is True
        assert "orders" in resp.json()

    def test_get_orders_unauthorized(self):
        """Получение заказов пользователя без авторизации"""
        resp = requests.get(f"{BASE_URL}/api/orders")
        assert resp.status_code == 401
        assert resp.json()["message"] == "You should be authorised"
