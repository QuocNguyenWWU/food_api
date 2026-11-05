from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app import services
from app.database import get_session
from app.schemas import FoodCreate, FoodRead

router = APIRouter(tags=["foods"])

@router.get("/foods", response_model=list[FoodRead])
def list_foods(category: str | None = None, available: bool | None = None, session: Session = Depends(get_session)):
    return services.list_foods(session, category, available)


@router.get("/foods/{food_id}", response_model=FoodRead)
def get_food(food_id: int, session: Session = Depends(get_session)):
    food = services.get_food(session, food_id)
    if food is None:
        raise HTTPException(status_code=404, detail="Food not found")
    return food


@router.post("/foods", response_model=FoodRead, status_code=201)
def add_food(food: FoodCreate, session: Session = Depends(get_session)):
    return services.create_food(session, food)


@router.get("/cheapfood", response_model=list[FoodRead])
def get_cheapfood(max_price: int = Query(default=30000, ge=0), session: Session = Depends(get_session)):
    return services.cheap_food(session, max_price)