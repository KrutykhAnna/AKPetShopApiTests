import pytest
import requests
import random

BASE_URL="http://5.181.109.28:9090/api/v3"

@pytest.fixture(scope="function")
def create_pet_fixture():
    """ Фикстура для создания питомца"""
    body = {
        "id": random.randrange(1,1000),
        "name": "Rex",
        "status": "available"
    }
    response = requests.post(url=f"{BASE_URL}/pet", json=body)
    assert response.status_code == 200
    return response.json()


@pytest.fixture(scope="function")
def create_new_order_fixture():
    """Фикстура создания заказа"""
    body = {
        "id": random.randrange(1,100),
        "petId": random.randrange(1,100),
        "quantity":  random.randrange(1,100),
        "status": random.choice(["approved", "placed", "delivered"]),
        "complete": random.choice([True,False])}
    response = requests.post(url=f"{BASE_URL}/store/order", json=body)
    assert response.status_code == 200
    return response.json()