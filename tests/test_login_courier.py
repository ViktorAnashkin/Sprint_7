import allure
import requests
from urls import Urls
from data.data import Data

@allure.story("Логин курьера")
class TestLoginCourier:
    @allure.title("Успешная авторизация курьера")
    def test_login_success(self, courier):
        courier_data, _ = courier
        response = requests.post(Urls.LOGIN_COURIER_URL, json={
            "login": courier_data["login"],
            "password": courier_data["password"]
        })
        assert response.status_code == 200
        assert "id" in response.json()

    @allure.title("Ошибка при неверном логине")
    def test_login_wrong_login(self, courier):
        courier_data, _ = courier
        response = requests.post(Urls.LOGIN_COURIER_URL, json={
            "login": "wronglogin",
            "password": courier_data["password"]
        })
        assert response.status_code == 404
        assert response.json()["message"] == Data.USER_NOT_FOUND

    @allure.title("Ошибка при неверном пароле")
    def test_login_wrong_password(self, courier):
        courier_data, _ = courier
        response = requests.post(Urls.LOGIN_COURIER_URL, json={
            "login": courier_data["login"],
            "password": "wrongpassword"
        })
        assert response.status_code == 404
        assert response.json()["message"] == Data.USER_NOT_FOUND

    @allure.title("Ошибка при отсутствии логина")
    def test_login_no_login(self, courier):
        courier_data, _ = courier
        response = requests.post(Urls.LOGIN_COURIER_URL, json={
            "login": "",
            "password": courier_data["password"]
        })
        assert response.status_code == 400
        assert response.json()["message"] == Data.LOGIN_DATA_MISSING

    @allure.title("Ошибка при отсутствии пароля")
    def test_login_no_password(self, courier):
        courier_data, _ = courier
        response = requests.post(Urls.LOGIN_COURIER_URL, json={
            "login": courier_data["login"],
            "password": ""
        })
        assert response.status_code == 400
        assert response.json()["message"] == Data.LOGIN_DATA_MISSING
        