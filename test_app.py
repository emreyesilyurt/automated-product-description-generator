import requests
import json

BASE_URL = "http://localhost:8000"

def test_health_check():
    response = requests.get(f"{BASE_URL}/health")
    assert response.status_code == 200
    assert response.json() == {"status": "OK"}

def test_generate_description():
    product_name = "TestProduct"
    payload = {"product_name": product_name}
    response = requests.post(f"{BASE_URL}/generate_description/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "description" in data
    assert "timestamp" in data

def test_get_descriptions():
    response = requests.get(f"{BASE_URL}/get_descriptions/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)

def test_get_description():
    product_name = "TestProduct"
    response = requests.get(f"{BASE_URL}/get_description/{product_name}")
    assert response.status_code == 200
    data = response.json()
    assert "description" in data
    assert "timestamp" in data
