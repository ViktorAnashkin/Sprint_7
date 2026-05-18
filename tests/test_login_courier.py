import allure
import pytest
import requests
from urls import Urls
from data.data import Data

@allure.story("Логин курьера")
class TestLoginCourier:
    @allure.title("Успешная авторизация курьера с корректными данными")
    def test_login_success(self, create_courier):
        courier_data = create_courier
        login_data = {
            "login": courier_data["login"],
            "password": courier_data["password"]
        }

        with allure.step("Попытка авторизации с корректными данными"):
            try:
                response = requests.post(Urls.LOGIN_COURIER_URL, json=login_data)
            except requests.RequestException as e:
                pytest.fail(f"Ошибка сети при выполнении запроса: {e}")


        with allure.step("Проверка статуса 200 (OK)"):
            assert response.status_code == 200, \
                f"Ожидался статус 200, получен {response.status_code}. Ответ: {response.text}"

        with allure.step("Проверка наличия поля 'id' в ответе"):
            try:
                assert "id" in response.json(), \
                    "В ответе успешного логина отсутствует поле 'id'. Ответ: {response.json()}"
            except ValueError as e:
                pytest.fail(f"Ответ не в формате JSON: {e}. Ответ: {response.text}")

    @allure.title("Тестирование сценариев ошибок при авторизации курьера")
    @pytest.mark.parametrize(
        "description,login_data,expected_status,expected_message",
        [
            (
                "Попытка авторизации с неверным логином",
                lambda courier_data: {
                    "login": "wronglogin",
            "password": courier_data["password"]
                },
                404,
                Data.USER_NOT_FOUND
            ),
            (
                "Попытка авторизации с неверным паролем",
                lambda courier_data: {
            "login": courier_data["login"],
            "password": "wrongpassword"
                },
                404,
                Data.USER_NOT_FOUND
            ),
            (
                "Попытка авторизации без логина (пустая строка)",
                lambda courier_data: {
            "login": "",
            "password": courier_data["password"]
                },
                400,
                Data.LOGIN_DATA_MISSING
            ),
            (
                "Попытка авторизации без пароля (пустая строка)",
                lambda courier_data: {
            "login": courier_data["login"],
            "password": ""
                },
                400,
                Data.LOGIN_DATA_MISSING
            )
        ]
    )
    def test_login_error_scenarios(self, create_courier, description, login_data, expected_status, expected_message):
        courier_data = create_courier
        final_login_data = login_data(courier_data)

        with allure.step(description):
            try:
                response = requests.post(Urls.LOGIN_COURIER_URL, json=final_login_data)
            except requests.RequestException as e:
                pytest.fail(f"Ошибка сети при выполнении запроса: {e}")


        with allure.step(f"Проверка статуса ответа — ожидается {expected_status}"):
            assert response.status_code == expected_status, \
                f"Статус ответа {response.status_code} не соответствует ожидаемому {expected_status}. Ответ: {response.text}"

        with allure.step("Проверка сообщения об ошибке"):
            try:
                actual_message = response.json().get("message")
                assert actual_message == expected_message, \
                    f"Ожидалось сообщение '{expected_message}', получено: '{actual_message}'. Ответ: {response.text}"
            except ValueError as e:
                pytest.fail(f"Ответ не в формате JSON: {e}. Ответ: {response.text}")
            except KeyError as e:
                pytest.fail(f"В ответе отсутствует ожидаемое поле: {e}. Ответ: {response.text}")
