import pytest
import requests
from data.urls import BASE_URL
from data.helpers import random_email, random_name

@pytest.fixture
def new_user():
    """Возвращает новые валидные данные пользователя"""
    return {
        "email": random_email(),
        "password": "TestPass123!",
        "name": random_name()
    }

@pytest.fixture
def register_user(new_user):
    """Создаёт пользователя и возвращает токены и данные"""
    url = f"{BASE_URL}/api/auth/register"
    resp = requests.post(url, json=new_user)
    resp.raise_for_status()
    tokens = {
        "access": resp.json()["accessToken"],
        "refresh": resp.json()["refreshToken"]
    }
    user_info = {"email": new_user["email"], "password": new_user["password"]}
    yield {**tokens, **user_info}
    headers = {"Authorization": tokens["access"]}
    requests.delete(f"{BASE_URL}/api/auth/user", headers=headers)

@pytest.fixture
def get_any_ingredient():
    """Возвращает один любой валидный id ингредиента"""
    url = f"{BASE_URL}/api/ingredients"
    resp = requests.get(url)
    resp.raise_for_status()
    data = resp.json()
    ingredient = data["data"][0]["_id"]
    return ingredient
