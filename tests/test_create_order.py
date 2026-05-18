import allure
import pytest
import requests
from urls import Urls
from data.data import order_black, order_gray, order_both, order_no_color


@allure.story("Создание заказа")
class TestCreateOrder:
    @allure.title("Создание заказа с разными цветами")
    @pytest.mark.parametrize("order_data,order_description", [
        (order_black, "Заказ с чёрным цветом"),
        (order_gray, "Заказ с серым цветом"),
        (order_both, "Заказ с чёрным и серым цветами"),
        (order_no_color, "Заказ без указания цвета")
    ])
    def test_create_order_success(self, order_data, order_description):
        with allure.step(f"Отправка запроса на создание заказа: {order_description}"):
            response = requests.post(Urls.ORDER_URL, json=order_data)

        with allure.step("Проверка статуса ответа — должен быть 201 (Created)"):
            assert response.status_code == 201

        with allure.step("Проверка наличия поля 'track' в ответе"):
            assert "track" in response.json()
