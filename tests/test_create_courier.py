import allure
import requests
from urls import Urls
from data.data import Data
from helpers import generate_random_string
import pytest

@allure.story("Создание курьера")
class TestCreateCourier:
    @allure.title("Успешное создание курьера")
    def test_create_courier_success(self):
        # Генерация данных для создания курьера внутри теста
        courier_data = {
            "login": generate_random_string(),
            "password": generate_random_string(),
            "firstName": generate_random_string(6)
        }

        with allure.step("Создание курьера через API"):
            response = requests.post(Urls.CREATE_COURIER_URL, json=courier_data)

        with allure.step("Проверка статуса 201 (Created)"):
            assert response.status_code == 201, \
                f"Ожидался статус 201, получен {response.status_code}. Ответ: {response.text}"

        with allure.step("Проверка ответа API {'ok': True}"):
            assert response.json() == {"ok": True}, \
                f"Некорректный ответ API: {response.json()}"

    @allure.title("Нельзя создать двух одинаковых курьеров")
    def test_create_duplicate_courier(self, create_courier):
        courier_data = create_courier

        with allure.step("Попытка создания курьера с дублирующим логином"):
            duplicate_response = requests.post(Urls.CREATE_COURIER_URL, json=courier_data)

        with allure.step("Проверка статуса 409 (Conflict)"):
            assert duplicate_response.status_code == 409, \
                f"Ожидался статус 409, получен {duplicate_response.status_code}"

        with allure.step("Проверка сообщения об ошибке 'duplicate login'"):
            assert duplicate_response.json().get("message") == Data.DUPLICATE_LOGIN, \
                f"Ожидалось сообщение '{Data.DUPLICATE_LOGIN}', получено: {duplicate_response.json().get('message')}"


    @allure.title("Ошибка при создании без логина")
    def test_create_courier_no_login(self):
        data = {"password": generate_random_string(), "firstName": generate_random_string(6)}


        with allure.step("Попытка создания курьера без логина"):
            response = requests.post(Urls.CREATE_COURIER_URL, json=data)

        with allure.step("Проверка статуса 400 (Bad Request)"):
            assert response.status_code == 400, \
                f"Ожидался статус 400, получен {response.status_code}"

        with allure.step("Проверка сообщения об ошибке 'missing fields'"):
            assert response.json().get("message") == Data.MISSING_FIELDS, \
                f"Ожидалось сообщение '{Data.MISSING_FIELDS}', получено: {response.json().get('message')}"

    @allure.title("Ошибка при создании без пароля")
    def test_create_courier_no_password(self):
        data = {"login": generate_random_string(), "firstName": generate_random_string(6)}

        with allure.step("Попытка создания курьера без пароля"):
            response = requests.post(Urls.CREATE_COURIER_URL, json=data)

        with allure.step("Проверка статуса 400 (Bad Request)"):
            assert response.status_code == 400, \
                f"Ожидался статус 400, получен {response.status_code}"

        with allure.step("Проверка сообщения об ошибке 'missing fields'"):
            assert response.json().get("message") == Data.MISSING_FIELDS, \
                f"Ожидалось сообщение '{Data.MISSING_FIELDS}', получено: {response.json().get('message')}"

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
            assert response.status_code == 409, \
                f"Ожидался статус 409, получен {response.status_code}"

        with allure.step("Проверка сообщения об ошибке 'duplicate login'"):
            assert response.json().get("message") == Data.DUPLICATE_LOGIN, \
                f"Ожидалось сообщение '{Data.DUPLICATE_LOGIN}', получено: {response.json().get('message')}"
