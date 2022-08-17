from typing import Optional

import uvicorn
from fastapi import FastAPI, HTTPException

from schemas import load_db, Car

app = FastAPI()

db = load_db()


@app.get("/")
def willkommen(name):
    """return a friendly welcome"""
    return {'message': f"Welcome {name}, to the Car Sharing Service!"}


@app.get("/api/cars")
def get_cars(size: Optional[str] = None, doors: Optional[int] = None) -> list:
    result = db
    if size:
        result = [car for car in result if car.size == size]
    if doors:
        result = [car for car in result if car.doors >= doors]
    return result


@app.get("/api/cars/{id}")
def car_by_id(id: int) -> Car:
    result = [car for car in db if car.id == id]
    if result:
        return result[0]
    else:
        raise HTTPException(status_code=404, detail=f"There is no car with id={id}.")


if __name__ == "__main__":
    uvicorn.run("car_sharing:app", reload=True)
