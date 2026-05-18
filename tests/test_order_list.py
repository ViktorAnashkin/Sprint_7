import allure
import requests
from urls import Urls

@allure.story("Список заказов")
class TestOrderList:
    @allure.title("Получение списка заказов")
    def test_get_order_list_success(self):
        with allure.step("Отправка GET‑запроса для получения списка заказов"):
            response = requests.get(Urls.ORDER_URL)

        with allure.step("Проверка статуса ответа — ожидается 200 (OK)"):
            assert response.status_code == 200

        with allure.step("Проверка наличия поля 'orders' в ответе"):
            assert "orders" in response.json()

        with allure.step("Проверка, что поле 'orders' содержит список"):
            assert isinstance(response.json()["orders"], list)
