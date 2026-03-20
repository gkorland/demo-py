import itertools

import pytest
from fastapi.testclient import TestClient
import main as app_module
from main import app


@pytest.fixture(autouse=True)
def reset_db():
    """Reset in-memory database and ID counter before each test."""
    app_module.db.clear()
    app_module._id_counter = itertools.count(1)
    yield


client = TestClient(app)

ITEM_PAYLOAD = {"name": "Widget", "description": "A useful widget", "price": 9.99, "in_stock": True}


def test_create_item():
    response = client.post("/items", json=ITEM_PAYLOAD)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "Widget"
    assert data["price"] == 9.99


def test_list_items_empty():
    response = client.get("/items")
    assert response.status_code == 200
    assert response.json() == []


def test_list_items():
    client.post("/items", json=ITEM_PAYLOAD)
    client.post("/items", json={**ITEM_PAYLOAD, "name": "Gadget", "price": 19.99})
    response = client.get("/items")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_item():
    client.post("/items", json=ITEM_PAYLOAD)
    response = client.get("/items/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Widget"


def test_get_item_not_found():
    response = client.get("/items/999")
    assert response.status_code == 404


def test_update_item():
    client.post("/items", json=ITEM_PAYLOAD)
    response = client.put("/items/1", json={"price": 14.99, "in_stock": False})
    assert response.status_code == 200
    data = response.json()
    assert data["price"] == 14.99
    assert data["in_stock"] is False
    assert data["name"] == "Widget"


def test_update_item_not_found():
    response = client.put("/items/999", json={"price": 5.0})
    assert response.status_code == 404


def test_delete_item():
    client.post("/items", json=ITEM_PAYLOAD)
    response = client.delete("/items/1")
    assert response.status_code == 204
    assert client.get("/items/1").status_code == 404


def test_delete_item_not_found():
    response = client.delete("/items/999")
    assert response.status_code == 404
