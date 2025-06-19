import pytest
import requests
import allure
from data.urls import BASE_URL
from data.texts import MSG_NO_INGREDIENTS

@allure.suite("Order API")
class TestOrderAPI:

    @allure.title("Создание заказа авторизованным пользователем")
    def test_create_order_authorized(self, register_user, get_any_ingredient):
        url = f"{BASE_URL}/api/orders"
        headers = {"Authorization": register_user["access"]}
        payload = {"ingredients": [get_any_ingredient]}
        resp = requests.post(url, json=payload, headers=headers)
        assert resp.status_code == 200
        assert resp.json()["success"] is True
        assert "order" in resp.json()

    @allure.title("Создание заказа неавторизованным пользователем")
    def test_create_order_unauthorized(self, get_any_ingredient):
        url = f"{BASE_URL}/api/orders"
        payload = {"ingredients": [get_any_ingredient]}
        resp = requests.post(url, json=payload)
        assert resp.status_code == 200
        assert resp.json()["success"] is True

    @allure.title("Создание заказа без ингредиентов")
    def test_create_order_no_ingredients(self, register_user):
        url = f"{BASE_URL}/api/orders"
        headers = {"Authorization": register_user["access"]}
        resp = requests.post(url, json={"ingredients": []}, headers=headers)
        assert resp.status_code == 400
        assert resp.json()["message"] == MSG_NO_INGREDIENTS

    @allure.title("Создание заказа с невалидным id ингредиента")
    def test_create_order_invalid_ingredient(self, register_user):
        url = f"{BASE_URL}/api/orders"
        headers = {"Authorization": register_user["access"]}
        resp = requests.post(url, json={"ingredients": ["invalid_id"]}, headers=headers)
        assert resp.status_code == 500 
