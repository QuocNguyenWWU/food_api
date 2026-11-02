from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Our "database": just a Python list in memory
foods = [
    {"id": 1, "name": "Pho bo", "price": 50000, "category": "noodle"},
    {"id": 2, "name": "Banh mi", "price": 25000, "category": "bread"},
    {"id": 3, "name": "Bun bo Hue", "price": 45000, "category": "noodle"},
    {"id": 4, "name": "Com tam", "price": 40000, "category": "rice"},
    {"id": 5, "name": "Bun cha", "price": 45000, "category": "noodle"},
    {"id": 6, "name": "Hu tieu", "price": 40000, "category": "noodle"},
    {"id": 7, "name": "Banh xeo", "price": 35000, "category": "snack"},
    {"id": 8, "name": "Goi cuon", "price": 30000, "category": "snack"},
    {"id": 9, "name": "Cha gio", "price": 30000, "category": "snack"},
    {"id": 10, "name": "Mi Quang", "price": 40000, "category": "noodle"},
    {"id": 11, "name": "Cao lau", "price": 45000, "category": "noodle"},
    {"id": 12, "name": "Bun rieu", "price": 35000, "category": "noodle"},
    {"id": 13, "name": "Xoi ga", "price": 25000, "category": "rice"},
    {"id": 14, "name": "Banh cuon", "price": 30000, "category": "snack"},
    {"id": 15, "name": "Chao long", "price": 30000, "category": "rice"},
    {"id": 16, "name": "Lau thai", "price": 250000, "category": "hotpot"},
    {"id": 17, "name": "Ca phe sua da", "price": 20000, "category": "drink"},
    {"id": 18, "name": "Tra da", "price": 5000, "category": "drink"},
    {"id": 19, "name": "Che ba mau", "price": 15000, "category": "dessert"},
    {"id": 20, "name": "Sinh to bo", "price": 30000, "category": "drink"},
]

class NewFood(BaseModel):
    name: str
    price: int
    category: str

@app.get("/")
def home():
    return {"message": "Hello! The food API is running."}


@app.get("/foods")
def list_foods(category: str | None = None):
    if category is None:
        return foods
    else:
        matching_foods = []
        for food in foods:
            if food["category"] == category.lower():
                matching_foods.append(food)
        return matching_foods

@app.get("/foods/{food_id}")
def get_food(food_id: int):
    for food in foods:
        if food["id"] == food_id:
            return food
    return {"error": "Food not found"}


@app.post("/foods")
def add_food(new_food: NewFood):
    food = {"id": len(foods) + 1, "name": new_food.name, "price": new_food.price, "category" : new_food.category.lower()}
    foods.append(food)
    return food


@app.get("/cheapfood")
def get_cheapfood(max_price: int = 30000):
    cheapfood = []
    for food in foods:
        if food["price"] < max_price:
            cheapfood.append(food)
    return cheapfood


