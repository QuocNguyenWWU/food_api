from fastapi import FastAPI

from app.routers import foods

app = FastAPI(title="Food API")
app.include_router(foods.router)


@app.get("/")
def home():
    return {"message": "Hello! The food API is running."}