from sqlalchemy import select
from database import SessionLocal
from models import Food

with SessionLocal() as session:
    foods = session.scalars(select(Food).where(Food.category == "drink").order_by(Food.id)).all()
    for food in foods:
        print(food.id, food.name, food.price, food.category)
