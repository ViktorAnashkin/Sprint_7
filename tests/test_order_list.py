import allure
import requests
from urls import Urls

@allure.story("Список заказов")
class TestOrderList:
    @allure.title("Получение списка заказов")
    def test_get_order_list_success(self):
        response = requests.get(Urls.ORDER_URL)
        assert response.status_code == 200
        assert "orders" in response.json()
        assert isinstance(response.json()["orders"], list)
        