import allure
import jsonschema
import pytest
import requests
from schemas.pet_schema import PET_SCHEMA

BASE_URL="http://5.181.109.28:9090/api/v3"

@allure.feature("Pet")
class TestPet:
    @allure.title("Попытка удалить несуществующего питомца")
    def test_delete_nonexistent_pet(self):
        with allure.step("Отправка запроса на удаление несуществующего питомца"):
            response = requests.delete(url=f"{BASE_URL}/pet/9999")
        with allure.step("Проверка status_code"):
            assert response.status_code == 200, (f"Ожидаемый результат: status_code == 200, "
                                                 f"Фактический результат: status_code == {response.status_code} ")
        with allure.step("Проверка текстового содержимого ответа"):
            assert response.text == "Pet deleted", (f"Ожидаемый результат: text == 'Pet deleted', "
                                                    f" Фактический результат: text == {response.text} ")

    @allure.title("Попытка обновить несуществующего питомца")
    def test_update_nonexistent_pet(self):
        with allure.step("Отправка запроса на обновление несуществующего питомца"):
            body = {
                "id": 9999,
                "name": "Non-existent Pet",
                "status": "available"
            }
            response = requests.put(url=f"{BASE_URL}/pet", json=body)
        with allure.step("Проверка status_code"):
            assert response.status_code == 404, (f"Ожидаемый результат: status_code == 404, "
                                                 f"Фактический результат: status_code == {response.status_code} ")
        with allure.step("Проверка текстового содержимого ответа"):
            assert response.text == "Pet not found", (f"Ожидаемый результат: text == 'Pet not found', "
                                                    f" Фактический результат: text == {response.text} ")

    @allure.title("Попытка получить информацию о несуществующем питомце")
    def test_get_nonexistent_pet(self):
        with allure.step("Отправка запроса на получение информации о несуществующем питомце"):
            response = requests.get(url=f"{BASE_URL}/pet/9999")
            with allure.step("Проверка status_code"):
                assert response.status_code == 404, (f"Ожидаемый результат: status_code == 404, "
                                                     f"Фактический результат: status_code == {response.status_code} ")
            with allure.step("Проверка текстового содержимого ответа"):
                assert response.text == "Pet not found", (f"Ожидаемый результат: text == 'Pet not found', "
                                                          f" Фактический результат: text == {response.text} ")

    @allure.title("Добавление нового питомца")
    def test_create_new_pet(self):
        with allure.step("Подготовка данных для создания питомца"):
            body = {
                "id": 15,
                "name": "Rex",
                "status": "available"
            }
        with allure.step("Отправка запроса на создание питомца"):
            response = requests.post(url=f"{BASE_URL}/pet", json=body)
            response_json = response.json()

        with allure.step("Проверка status_code и валидация JSON-схемы"):
            assert response.status_code == 200, (f"Ожидаемый результат: status_code == 200, "
                                                 f"Фактический результат: status_code == {response.status_code} ")
            jsonschema.validate(response_json,PET_SCHEMA)

        with allure.step("Проверка параметров питомца"):
            assert  response_json["id"] == body["id"], (f"Ожидаемый результат: id == {body["id"]},"
                                                        f" Фактический результат: id == {response_json["id"]}")
            assert response_json["name"] == body["name"], (f"Ожидаемый результат: name == {body["name"]},"
                                                       f" Фактический результат: name == {response_json["name"]}")
            assert response_json["status"] == body["status"], (f"Ожидаемый результат: status == {body["status"]},"
                                                       f" Фактический результат: status == {response_json["status"]}")

    @allure.title("Добавление нового питомца c полными данными")
    def test_create_pet_with_full_data(self):
        with allure.step("Подготовка данных для создания питомца"):
            body = {
                "id": 10,
                "name": "doggie",
                "category": {"id": 1, "name": "Dogs"},
                "photoUrls": ["string"],
                "tags": [{"id": 0, "name": "string"}],
                "status": "available"
            }

        with allure.step("Отправка запроса на создание питомца"):
            response = requests.post(url=f"{BASE_URL}/pet", json=body)
            response_json = response.json()

        with allure.step("Проверка status_code и валидация JSON-схемы"):
            assert response.status_code == 200, (f"Ожидаемый результат: status_code == 200, "
                                                 f"Фактический результат: status_code == {response.status_code} ")
            jsonschema.validate(response_json, PET_SCHEMA)

        with allure.step("Проверка параметров питомца"):
            assert response_json["id"] == body["id"], (f"Ожидаемый результат: id == {body["id"]},"
                                                       f" Фактический результат: id == {response_json["id"]}")
            assert response_json["name"] == body["name"], (f"Ожидаемый результат: name == {body["name"]},"
                                                           f" Фактический результат: name == {response_json["name"]}")
            assert response_json["category"] == body["category"], (f"Ожидаемый результат: category == {body["category"]},"
                                                           f" Фактический результат: category == {response_json["category"]}")
            assert response_json["photoUrls"] == body["photoUrls"], (f"Ожидаемый результат: photoUrls == {body["photoUrls"]}, "
                                                                   f"Фактический результат: photoUrls == {response_json["photoUrls"]}")
            assert response_json["tags"] == body["tags"], (f"Ожидаемый результат: tags == {body["tags"]}, "
                                                                     f"Фактический результат: tags == {response_json["tags"]}")
            assert response_json["status"] == body["status"], (f"Ожидаемый результат: status == {body["status"]},"
                                                               f" Фактический результат: status == {response_json["status"]}")

    @allure.title("Получение информации о питомце по id")
    def test_get_pet_by_id(self,
                           create_pet_fixture: dict):
        with allure.step("Получение id созданного питомца"):
            pet_id = create_pet_fixture["id"]

        with allure.step("Отправка запроса на получение информации о питомце по id"):
            response = requests.get(url=f"{BASE_URL}/pet/{pet_id}")
            response_dict = response.json()
            with allure.step("Проверка статуса ответа и данных питомца"):
                assert response.status_code == 200, (f"Ожидаемый результат: status_code == 200, "
                                                     f"Фактический результат: status_code == {response.status_code} ")
                assert response_dict["id"] == pet_id, (f"Ожидаемый результат id == {pet_id}, "
                                                       f"Фактический результат id == {response_dict["id"]}")
                assert response_dict["name"] == create_pet_fixture["name"], (
                    f"Ожидаемый результат name == {create_pet_fixture["name"]}, "
                    f"Фактический результат name == {response_dict["name"]}")
                assert response_dict["status"] == create_pet_fixture["status"], (
                    f"Ожидаемый результат: status == {create_pet_fixture["status"]} ,"
                    f" Фактический результат: status == {response_dict["status"]}")

    @allure.title("Получение списка питомцев по статусу")
    @pytest.mark.parametrize("status, expected_status_code",[
         ("available",200),
         ("invalid",400),
         ("sold",200),
         ("",400)])
    def test_get_pets_by_status(self, status: str, expected_status_code: int):
        with allure.step(f"Отправка запрос на получение питомцев по статусу {status}"):
            response = requests.get(url=f"{BASE_URL}/pet/findByStatus", params={"status": status})
            response_dict = response.json()
        with allure.step("Проверка статуса ответа"):
            assert response.status_code == expected_status_code, (f"Ожидаемый результат: status_code == {expected_status_code}, "
                                                 f"Фактический результат: status_code == {response.status_code} ")
        with allure.step("Проверка формата данных и корректности ответа"):
            if response.status_code == 200:
                assert isinstance(response_dict, list), (f"Ожидаемый результат: type == list, "
                                                 f"Фактический результат: type == {type(response_dict)} ")
                assert response_dict[0]["status"] == status
            else:
                assert response_dict["message"] == f"Input error: query parameter `status value `{status}` is not in the allowable values `[available, pending, sold]`"


    @allure.title("Обновление информации о питомце")
    def test_update_pet(self,
                        create_pet_fixture: dict):
        with allure.step("Получение id созданного питомца"):
            pet_id = create_pet_fixture["id"]

        with allure.step("Отправка запроса на обновление питомца"):
            body = {
                "id": pet_id,
                "name": "Buddy Updated",
                "status": "sold"
            }
            response = requests.put(url=f"{BASE_URL}/pet", json=body)
            response_dict = response.json()

        with allure.step("Проверка статуса ответа и обновленные данные питомца"):
            assert response.status_code == 200, (f"Ожидаемый результат: status_code == 200, "
                                                 f"Фактический результат: status_code == {response.status_code} ")
            assert response_dict["id"]  == pet_id, (f"Ожидаемый результат: id == {pet_id}, "
                                                     f"Фактический результат: id == {response_dict["id"]}")
            assert response_dict["name"] == body["name"], (f"Ожидаемый результат: name == {body["name"]}, "
                                                           f"Фактический результат: name == {response_dict["name"]}")
            assert response_dict["status"] == body["status"], (f"Ожидаемый результат: status == {body["status"]} ,"
                                                               f"Фактический результат: status == {response_dict["status"]}")

    @allure.title("Удаление питомца по id")
    def test_delete_pet(self,
                        create_pet_fixture: dict):
        with allure.step("Получение id созданного питомца"):
            pet_id = create_pet_fixture["id"]

        with allure.step("Отправка запроса на удаление питомца"):
            response = requests.delete(url=f"{BASE_URL}/pet/{pet_id}")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, (f"Ожидаемый результат: status_code == 200, "
                                                 f"Фактический результат: status_code == {response.status_code} ")

        with allure.step("Попытка получить данные удаленного питомца"):
            response = requests.get(url=f"{BASE_URL}/pet/{pet_id}")
            assert response.status_code == 404, (f"Ожидаемый результат: status_code == 404, "
                                                 f"Фактический результат: status_code == {response.status_code} ")
            assert response.text == "Pet not found", (f"Ожидаемый результат: text == 'Pet not found' ,"
                                                    f" Фактический результат: text == {response.text} ")