import pytest
import requests
import random

BASE_URL = "http://5.181.109.28:9090/api/v3"

@pytest.fixture(scope="function")
def create_new_order_fixture():
    """Фикстура создания заказа"""
    body = {
        "id": random.randrange(1,100),
        "petId": 1,
        "quantity": 1,
        "status": random.choice(["approved", "placed", "delivered"]),
        "complete": True}
    response = requests.post(url=f"{BASE_URL}/store/order", json=body)
    assert response.status_code == 200
    return response.json()
