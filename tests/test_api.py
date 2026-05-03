import pytest
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)


# ============ Sandwich Tests ============

def test_create_sandwich():
    response = client.post("/sandwiches/", json={
        "sandwich_name": "Test Sandwich",
        "price": 5.99
    })
    assert response.status_code == 200
    data = response.json()
    assert data["sandwich_name"] == "Test Sandwich"
    assert data["price"] == 5.99
    assert "id" in data


def test_get_all_sandwiches():
    response = client.get("/sandwiches/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_one_sandwich():
    # First create a sandwich
    create_response = client.post("/sandwiches/", json={
        "sandwich_name": "Get Test Sandwich",
        "price": 4.99
    })
    sandwich_id = create_response.json()["id"]

    # Then get it
    get_response = client.get(f"/sandwiches/{sandwich_id}")
    assert get_response.status_code == 200
    assert get_response.json()["id"] == sandwich_id


def test_get_sandwich_not_found():
    response = client.get("/sandwiches/99999")
    assert response.status_code == 404


def test_update_sandwich():
    # First create
    create_response = client.post("/sandwiches/", json={
        "sandwich_name": "Update Test",
        "price": 1.99
    })
    sandwich_id = create_response.json()["id"]

    # Then update
    update_response = client.put(f"/sandwiches/{sandwich_id}", json={
        "price": 3.99
    })
    assert update_response.status_code == 200
    assert update_response.json()["price"] == 3.99


def test_delete_sandwich():
    # First create
    create_response = client.post("/sandwiches/", json={
        "sandwich_name": "Delete Test",
        "price": 1.99
    })
    sandwich_id = create_response.json()["id"]

    # Then delete
    delete_response = client.delete(f"/sandwiches/{sandwich_id}")
    assert delete_response.status_code == 204

    # Verify it's gone
    get_response = client.get(f"/sandwiches/{sandwich_id}")
    assert get_response.status_code == 404


# ============ Resource Tests ============

def test_create_resource():
    response = client.post("/resources/", json={
        "item": "Test Resource",
        "amount": 10
    })
    assert response.status_code == 200
    data = response.json()
    assert data["item"] == "Test Resource"
    assert "id" in data


def test_get_all_resources():
    response = client.get("/resources/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_one_resource():
    # First create
    create_response = client.post("/resources/", json={
        "item": "Get Test Resource",
        "amount": 5
    })
    resource_id = create_response.json()["id"]

    # Then get
    get_response = client.get(f"/resources/{resource_id}")
    assert get_response.status_code == 200
    assert get_response.json()["id"] == resource_id


def test_get_resource_not_found():
    response = client.get("/resources/99999")
    assert response.status_code == 404


def test_update_resource():
    # First create
    create_response = client.post("/resources/", json={
        "item": "Update Test Resource",
        "amount": 10
    })
    resource_id = create_response.json()["id"]

    # Then update
    update_response = client.put(f"/resources/{resource_id}", json={
        "amount": 25
    })
    assert update_response.status_code == 200
    assert update_response.json()["amount"] == 25


def test_delete_resource():
    # First create
    create_response = client.post("/resources/", json={
        "item": "Delete Test Resource",
        "amount": 100
    })
    resource_id = create_response.json()["id"]

    # Then delete
    delete_response = client.delete(f"/resources/{resource_id}")
    assert delete_response.status_code == 204

    # Verify it's gone
    get_response = client.get(f"/resources/{resource_id}")
    assert get_response.status_code == 404