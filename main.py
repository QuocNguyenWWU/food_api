from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict, Field, field_validator
from sqlalchemy import select
from database import SessionLocal
from models import Food

app = FastAPI()


class FoodCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(min_length=1)
    price: int = Field(ge=0)
    category: str = Field(min_length=1)
    is_available: bool = Field(default=True)

    @field_validator("name", "category")
    @classmethod
    def collapse_spaces(cls, value: str) -> str:
        return " ".join(value.split())

    @field_validator("category")
    @classmethod
    def lowercase_category(cls, value: str) -> str:
        return value.lower()


class FoodRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    price: int
    category: str
    is_available: bool


@app.get("/")
def home():
    return {"message": "Hello! The food API is running."}


@app.get("/foods", response_model=list[FoodRead])
def list_foods(category: str | None = None, available: bool | None = None):
    if category:
        category = category.strip().lower()
    query = select(Food).order_by(Food.id)
    if category:
        query = query.where(Food.category == category)
    if available is not None:
        query = query.where(Food.is_available == available)
    with SessionLocal() as session:
        return session.scalars(query).all()


@app.get("/foods/{food_id}", response_model=FoodRead)
def get_food(food_id: int):
    with SessionLocal() as session:
        food = session.get(Food, food_id)
    if food is None:
        raise HTTPException(status_code=404, detail="Food not found")
    return food


@app.post("/foods", response_model=FoodRead, status_code=201)
def add_food(food: FoodCreate):
    new_food = Food(name=food.name, price=food.price, category=food.category, is_available=food.is_available)
    with SessionLocal() as session:
        session.add(new_food)
        session.commit()
        session.refresh(new_food)
    return new_food


@app.get("/cheapfood")
@app.get("/cheapfood", response_model=list[FoodRead])
def get_cheapfood(max_price: int = 30000):
    query = select(Food).where(Food.price < max_price).order_by(Food.id)
    with SessionLocal() as session:
        return session.scalars(query).all()
