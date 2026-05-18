import allure
import requests
from urls import Urls
from data.data import Data
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


@allure.story("Создание курьера")
class TestCreateCourier:
    @allure.title("Успешное создание курьера")
    def test_create_courier_success(self, create_courier):
        with allure.step("Проверка, что курьер успешно создан фикстурой"):
            courier_data = create_courier
            assert courier_data is not None

    @allure.title("Нельзя создать двух одинаковых курьеров")
    def test_create_duplicate_courier(self, create_courier):
        courier_data = create_courier

        with allure.step("Попытка создания курьера с дублирующим логином"):
            duplicate_response = requests.post(Urls.CREATE_COURIER_URL, json=courier_data)

        with allure.step("Проверка статуса 409 (Conflict)"):
            assert duplicate_response.status_code == 409

        with allure.step("Проверка сообщения об ошибке 'duplicate login'"):
            assert duplicate_response.json()["message"] == Data.DUPLICATE_LOGIN


    @allure.title("Ошибка при создании без логина")
    def test_create_courier_no_login(self):
        data = {"password": generate_random_string(), "firstName": generate_random_string(6)}

        with allure.step("Попытка создания курьера без логина"):
            response = requests.post(Urls.CREATE_COURIER_URL, json=data)

        with allure.step("Проверка статуса 400 (Bad Request)"):
            assert response.status_code == 400

        with allure.step("Проверка сообщения об ошибке 'missing fields'"):
            assert response.json()["message"] == Data.MISSING_FIELDS

    @allure.title("Ошибка при создании без пароля")
    def test_create_courier_no_password(self):
        data = {"login": generate_random_string(), "firstName": generate_random_string(6)}

        with allure.step("Попытка создания курьера без пароля"):
            response = requests.post(Urls.CREATE_COURIER_URL, json=data)

        with allure.step("Проверка статуса 400 (Bad Request)"):
            assert response.status_code == 400

        with allure.step("Проверка сообщения об ошибке 'missing fields'"):
            assert response.json()["message"] == Data.MISSING_FIELDS

    @allure.title("Ошибка при создании с существующим логином")
    def test_create_courier_existing_login(self, create_courier):
        courier_data = create_courier
        new_data = {
            "login": courier_data["login"],
            "password": generate_random_string(),
            "firstName": generate_random_string(6)
        }

        with allure.step("Попытка создания курьера с существующим логином"):
            response = requests.post(Urls.CREATE_COURIER_URL, json=new_data)

        with allure.step("Проверка статуса 409 (Conflict)"):
            assert response.status_code == 409

        with allure.step("Проверка сообщения об ошибке 'duplicate login'"):
            assert response.json()["message"] == Data.DUPLICATE_LOGIN
