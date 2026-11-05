from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_home_says_hello():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello! The food API is running."}


def test_negative_price_is_rejected():
    response = client.post("/foods", json={"name": "Bad food", "price": -5, "category": "snack"})
    assert response.status_code == 422


def test_food_id_must_be_a_number():
    response = client.get("/foods/abc")
    assert response.status_code == 422


def test_name_with_only_spaces_is_rejected():
    response = client.post("/foods", json={"name": "    ", "price": 5, "category": "snack"})
    assert response.status_code == 422


def test_empty_category_is_rejected():
    response = client.post("/foods", json={"name": "hu tieu", "price": 5, "category": ""})
    assert response.status_code == 422


def test_category_is_missing_is_rejected():
    response = client.post("/foods", json={"name": "hu tieu", "price": 5})
    assert response.status_code == 422


def test_max_price_must_be_a_number():
    response = client.get("/cheapfood?max_price=abc")
    assert response.status_code == 422


def test_negative_max_price_is_rejected():
    response = client.post("/cheapfood?max_price=-5000")
    assert response.status_code == 405
