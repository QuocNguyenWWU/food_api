def test_create_then_read_food(client):
    created = client.post("/foods", json={"name": "  Tra   da ", "price": 5000, "category": " Drink "})
    assert created.status_code == 201
    food = created.json()
    assert food["name"] == "Tra da"
    assert food["category"] == "drink"
    assert food["is_available"] is True

    response = client.get(f"/foods/{food['id']}")
    assert response.status_code == 200
    assert response.json() == food


def test_missing_food_returns_404(client):
    response = client.get("/foods/999")
    assert response.status_code == 404


def test_each_test_starts_with_empty_database(client):
    assert client.get("/foods").json() == []


def test_each_test_ends_with_empty_database(client):
    assert client.get("/foods").json() == []


def test_filter_unavailable_foods(client):
    client.post("/foods", json={"name": "  Tra   da ", "price": 5000, "category": " Drink "})
    unavailable = client.post("/foods", json={"name": "  Com suon ", "price": 25000, "category": " rice ",
                                              "is_available": False}).json()

    response = client.get("/foods?available=false")
    assert response.status_code == 200
    assert response.json() == [unavailable]


def test_cheapfood_returns_only_foods_under_max_price(client):
    cheapfood = client.post("/foods", json={"name": "  Tra   da ", "price": 20000, "category": " Drink "}).json()
    client.post("/foods", json={"name": "  Com suon ", "price": 40000, "category": " rice ",
                                              "is_available": True})

    response = client.get("/cheapfood?max_price=30000")
    assert response.status_code == 200
    assert response.json() == [cheapfood]