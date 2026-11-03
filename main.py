import os
import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict, Field


app = FastAPI()

class NewFood(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(min_length=1)
    price: int = Field(ge=0)
    category: str = Field(min_length=1)


load_dotenv()
DATABASE_URL = os.environ["DATABASE_URL"]


def get_conn():
    return psycopg.connect(DATABASE_URL, row_factory=dict_row)


@app.get("/")
def home():
    return {"message": "Hello! The food API is running."}


@app.get("/foods")
def list_foods(category: str | None = None):
    with get_conn() as conn:
        if category is None:
            return conn.execute(
                "SELECT id, name, price, category FROM foods ORDER BY id"
            ).fetchall()
        return conn.execute(
            "SELECT id, name, price, category FROM foods WHERE category = %s ORDER BY id",
            (category.strip().lower(),),
        ).fetchall()


@app.get("/foods/{food_id}")
def get_food(food_id: int):
    with get_conn() as conn:
        result = conn.execute(
            "SELECT id, name, price, category FROM foods WHERE id = %s", (food_id,)
        ).fetchone()
    if result is None:
        raise HTTPException(status_code=404, detail="Food not found")
    return result


@app.post("/foods")
def add_food(food: NewFood):
    with get_conn() as conn:
        result = conn.execute(
            """INSERT INTO foods (name, price, category) 
            VALUES (%s, %s, %s) 
            RETURNING id, name, price, category""", (food.name, food.price, food.category.lower())
        ).fetchone()
    return result


@app.get("/cheapfood")
def get_cheapfood(max_price: int = 30000):
    with get_conn() as conn:
        result = conn.execute(
            """
            SELECT id, name, price, category 
            FROM foods 
            WHERE price < %s
            ORDER BY id
            """, (max_price,)
        ).fetchall()
    return result
