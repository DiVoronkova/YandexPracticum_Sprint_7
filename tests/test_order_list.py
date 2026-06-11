import allure
from api_methods.order_methods import OrderMethods


class TestOrderList:

    @allure.title("Тест успешного полученея списка заказов")
    @allure.description("Тест проверяет, что система возвращает статус‑код 200 и правильное тело списка заказов")
    def test_get_order_list(self):
        response = OrderMethods.get_order_list()
        json_data = response.json()
        assert response.status_code == 200, f"Ожидался код 200, но получен {response.status_code}"
        for order in json_data["orders"]:
            assert "id" in order, "В заказе отсутствует поле 'id'"
            assert "courierId" in order, "В заказе отсутствует поле 'courierId'"
            assert "firstName" in order, "В заказе отсутствует поле 'firstName'"
            assert "lastName" in order, "В заказе отсутствует поле 'lastName'"
            assert "address" in order, "В заказе отсутствует поле 'address'"
            assert "metroStation" in order, "В заказе отсутствует поле 'metroStation'"
            assert "phone" in order, "В заказе отсутствует поле 'phone'"
            assert "rentTime" in order, "В заказе отсутствует поле 'rentTime'"
            assert "deliveryDate" in order, "В заказе отсутствует поле 'deliveryDate'"
            assert "track" in order, "В заказе отсутствует поле 'track'"
            assert "color" in order, "В заказе отсутствует поле 'color'"
            assert "comment" in order, "В заказе отсутствует поле 'comment'"
            assert "createdAt" in order, "В заказе отсутствует поле 'createdAt'"
            assert "updatedAt" in order, "В заказе отсутствует поле 'updatedAt'"
            assert "status" in order, "В заказе отсутствует поле 'status'"


