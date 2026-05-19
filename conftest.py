import allure
import requests
from urls import Urls
from helpers import generate_random_string
import pytest

@pytest.fixture
def create_courier():
    """Фикстура для создания и автоматического удаления курьера после теста"""
    courier_data = {
        "login": generate_random_string(),
        "password": generate_random_string(),
        "firstName": generate_random_string(6)
    }

    with allure.step("Создание курьера через API"):
        response = requests.post(Urls.CREATE_COURIER_URL, json=courier_data)
        assert response.status_code == 201
        assert response.json() == {"ok": True}

    yield courier_data

    with allure.step("Удаление курьера после завершения теста"):
        login_response = requests.post(
            Urls.LOGIN_COURIER_URL,
            json={
                "login": courier_data["login"],
                "password": courier_data["password"]
            }
        )
        if login_response.status_code == 200 and "id" in login_response.json():
            courier_id = login_response.json()["id"]
            requests.delete(f"{Urls.CREATE_COURIER_URL}/{courier_id}")
