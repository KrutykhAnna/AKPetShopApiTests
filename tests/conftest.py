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