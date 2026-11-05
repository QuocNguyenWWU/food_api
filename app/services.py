from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models import Food
from app.schemas import FoodCreate


def get_food(session: Session, food_id: int) -> Food | None:
    return session.get(Food, food_id)


def create_food(session: Session, data: FoodCreate) -> Food:
    food = Food(name=data.name, price=data.price, category=data.category, is_available=data.is_available)
    session.add(food)
    session.commit()
    session.refresh(food)
    return food


def list_foods(session: Session, category: str | None = None, available: bool | None = None) -> list[Food]:
    if category:
        category = category.strip().lower()
    query = select(Food).order_by(Food.id)
    if category:
        query = query.where(Food.category == category)
    if available is not None:
        query = query.where(Food.is_available == available)
    return session.scalars(query).all()


def cheap_food(session: Session, max_price: int) -> list[Food]:
    query = select(Food).where(Food.price < max_price).order_by(Food.id)
    return session.scalars(query).all()
