import allure
import jsonschema
import requests
from requests import Response

from schemas.store_schema import INVENTORY_STORE_SCHEMA, STORE_SCHEMA

BASE_URL = "http://5.181.109.28:9090/api/v3"


@allure.feature("Store")
class TestStore:
    def _validate_response(self,
                           response: Response,
                           expected_code: int,
                           schema: dict | None = None):
        assert response.status_code == expected_code, (f"Ожидаемый результат: status_code == {expected_code}, "
                                                       f"Фактический результат: status_code == {response.status_code} ")
        if expected_code == 200:
            if schema:
                jsonschema.validate(response.json(), schema)
            return response.json()
        return None

    def _assert_order_data(self,
                           response_data: dict,
                           expected_data: dict):
        """Метод для проверки данных заказа"""
        assert response_data["id"] == expected_data["id"], (
            f"Ожидаемый результат: id == {expected_data["id"]}, "
            f"Фактический результат: id == {response_data["id"]} "
        )
        assert response_data["petId"] == expected_data["petId"], (
            f"Ожидаемый результат: petId == {expected_data["petId"]}, "
            f"Фактический результат: petId == {response_data["petId"]} "
        )
        assert response_data["quantity"] == expected_data["quantity"], (
            f"Ожидаемый результат: quantity == {expected_data["quantity"]}, "
            f"Фактический результат: quantity == {response_data["quantity"]} "
        )
        assert response_data["status"] == expected_data["status"], (
            f"Ожидаемый результат: status == {expected_data["status"]}, "
            f"Фактический результат: status == {response_data["status"]} "
        )
        assert response_data["complete"] == expected_data["complete"], (
            f"Ожидаемый результат: complete == {expected_data["complete"]}, "
            f"Фактический результат: complete == {response_data["complete"]} "
        )

    def _get_order_and_validate(self,
                                    order_id: int,
                                    expected_code: int,
                                    schema: dict | None = None):
        response = requests.get(url=f"{BASE_URL}/store/order/{order_id}")
        with allure.step("Проверка status_code и валидация JSON-схемы"):
            response_dict = self._validate_response(response, expected_code, schema)
        return response_dict

    @allure.title("Размещение заказа")
    def test_create_order(self):
        with allure.step("Отправка запроса на создание заказа"):
            body = {
                "id": 1,
                "petId": 1,
                "quantity": 1,
                "status": "placed",
                "complete": True}
            response = requests.post(url=f"{BASE_URL}/store/order", json=body)

        with allure.step("Проверка status_code и валидация JSON-схемы"):
            self._validate_response(response, 200, STORE_SCHEMA)

        with allure.step("Проверка данных заказа"):
            self._assert_order_data(response.json(), body)

    @allure.title("Получение информации о заказе по ID")
    def test_get_order_by_id(self,
                             create_new_order_fixture: dict):
        with allure.step("Получение id созданного заказа"):
            order_id = create_new_order_fixture["id"]

        with allure.step("Отправка запроса на получение информации о заказе по id"):
            response_data = self._get_order_and_validate(order_id, 200, STORE_SCHEMA)

        with allure.step("Проверка данных заказа"):
            self._assert_order_data(response_data, create_new_order_fixture)

    @allure.title("Удаление заказа по ID")
    def test_delete_order_by_id(self,
                                create_new_order_fixture: dict):
        with allure.step("Получение id созданного заказа"):
            order_id = create_new_order_fixture["id"]

        with allure.step("Отправка запроса на удаление заказе по id"):
            response = requests.delete(url=f"{BASE_URL}/store/order/{order_id}")

        with allure.step("Проверка status_code и валидация JSON-схемы"):
            response_data = self._validate_response(response, 200, STORE_SCHEMA)

        with allure.step("Проверка, что данные удаленного заказа соответствуют созданному"):
            self._assert_order_data(response_data, create_new_order_fixture)

        with allure.step("Отправка запроса на получение данных удаленного заказа"):
            self._get_order_and_validate(order_id, 404)

    @allure.title("Попытка получить информацию о несуществующем заказе")
    def test_get_nonexistent_order(self):
        with allure.step("Отправка запроса на получение информации о несуществующем заказе"):
            self._get_order_and_validate(9999, 404)

    @allure.title("Получение инвентаря магазина")
    def test_get_store_inventory(self):
        with allure.step("Отправка запроса на получение инвентаря магазина"):
            response = requests.get(url=f"{BASE_URL}/store/inventory")

        with allure.step("Проверка status_code и валидация JSON-схемы"):
            self._validate_response(response, 200, INVENTORY_STORE_SCHEMA)
