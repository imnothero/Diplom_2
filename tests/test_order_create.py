import pytest
import requests

BASE_URL = "https://stellarburgers.nomoreparties.site"

class TestOrderAPI:

    def test_create_order_authorized(self, register_user, get_any_ingredient):
        """Создание заказа авторизованным пользователем"""
        url = f"{BASE_URL}/api/orders"
        headers = {"Authorization": register_user["access"]}
        payload = {"ingredients": [get_any_ingredient]}
        resp = requests.post(url, json=payload, headers=headers)
        assert resp.status_code == 200
        assert resp.json()["success"] is True
        assert "order" in resp.json()

    def test_create_order_unauthorized(self, get_any_ingredient):
        """Создание заказа неавторизованным пользователем"""
        url = f"{BASE_URL}/api/orders"
        payload = {"ingredients": [get_any_ingredient]}
        resp = requests.post(url, json=payload)
        assert resp.status_code == 200
        assert resp.json()["success"] is True

    def test_create_order_no_ingredients(self, register_user):
        """Создание заказа без ингредиентов"""
        url = f"{BASE_URL}/api/orders"
        headers = {"Authorization": register_user["access"]}
        resp = requests.post(url, json={"ingredients": []}, headers=headers)
        assert resp.status_code == 400
        assert resp.json()["message"] == "Ingredient ids must be provided"

    def test_create_order_invalid_ingredient(self, register_user):
        """Создание заказа с невалидным id ингредиента"""
        url = f"{BASE_URL}/api/orders"
        headers = {"Authorization": register_user["access"]}
        resp = requests.post(url, json={"ingredients": ["invalid_id"]}, headers=headers)
        assert resp.status_code == 500  # Это особенность API
