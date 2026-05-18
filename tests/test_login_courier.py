import allure
import pytest
import requests
from urls import Urls
from data.data import Data

@allure.story("Логин курьера")
class TestLoginCourier:
    @allure.title("Тестирование различных сценариев авторизации курьера")
    @pytest.mark.parametrize(
        "login_data,expected_status,expected_message,allure_description",
        [
            (
                lambda courier_data: {
                    "login": courier_data["login"],
            "password": courier_data["password"]
                },
                200,
                None,
                "Успешная авторизация курьера с корректными данными"
            ),
            (
                lambda courier_data: {
            "login": "wronglogin",
            "password": courier_data["password"]
                },
                404,
                Data.USER_NOT_FOUND,
                "Попытка авторизации с неверным логином"
            ),
            (
                lambda courier_data: {
            "login": courier_data["login"],
            "password": "wrongpassword"
                },
                404,
                Data.USER_NOT_FOUND,
                "Попытка авторизации с неверным паролем"
            ),
            (
                lambda courier_data: {
            "login": "",
            "password": courier_data["password"]
                },
                400,
                Data.LOGIN_DATA_MISSING,
                "Попытка авторизации без логина (пустая строка)"
            ),
            (
                lambda courier_data: {
            "login": courier_data["login"],
            "password": ""
                },
                400,
                Data.LOGIN_DATA_MISSING,
                "Попытка авторизации без пароля (пустая строка)"
            )
        ]
    )
    def test_login_scenarios(self, courier, login_data, expected_status, expected_message, allure_description):
        courier_data, _ = courier
        final_login_data = login_data(courier_data)

        with allure.step(allure_description):
            response = requests.post(Urls.LOGIN_COURIER_URL, json=final_login_data)

        with allure.step(f"Проверка статуса ответа — ожидается {expected_status}"):
            assert response.status_code == expected_status

        if expected_message is None:
            with allure.step("Для успешного входа проверяем наличие поля 'id' в ответе"):
                assert "id" in response.json()
        else:
            with allure.step("Проверка сообщения об ошибке в ответе"):
                assert response.json()["message"] == expected_message
