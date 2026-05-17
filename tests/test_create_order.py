import allure
import pytest
import requests
from urls import Urls
from data.data import order_black, order_gray, order_both, order_no_color

@allure.story("Создание заказа")
class TestCreateOrder:
    @allure.title("Создание заказа с разными цветами")
    @pytest.mark.parametrize("order_data", [order_black, order_gray, order_both, order_no_color])
    def test_create_order_success(self, order_data):
        response = requests.post(Urls.ORDER_URL, json=order_data)
        assert response.status_code == 201
        assert "track" in response.json()
        