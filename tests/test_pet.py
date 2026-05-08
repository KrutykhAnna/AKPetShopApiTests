import random

import allure
import requests

BASE_URL="http://5.181.109.28:9090/api/v3"

@allure.feature("Pet")
class TestPet:
    @allure.title("Попытка удалить несуществующего питомца")
    def test_delete_nonexistent_pet(self):
        with allure.step("Отправка запроса на удаление несуществующего питомца"):
            response = requests.delete(url=f"{BASE_URL}/pet/{random.randrange(1000,10000)}")
        with allure.step("Проверка status_code"):
            assert response.status_code == 200, (f"Ожидаемый результат: status_code == 200, "
                                                 f"Фактический результат: status_code == {response.status_code} ")
        with allure.step("Проверка текстового содержимого ответа"):
            assert response.text == "Pet deleted", (f"Ожидаемый результат: text == 'Pet deleted', "
                                                    f" Фактический результат: text == {response.text} ")

