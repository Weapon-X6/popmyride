from typing import Optional

import uvicorn
from fastapi import FastAPI, HTTPException

from schemas import load_db, CarInput, save_db, CarOutput

app = FastAPI()

db = load_db()


@app.get("/api/cars")
def get_cars(size: Optional[str] = None, doors: Optional[int] = None) -> list:
    result = db
    if size:
        result = [car for car in result if car.size == size]
    if doors:
        result = [car for car in result if car.doors >= doors]
    return result


@app.get("/api/cars/{id}")
def car_by_id(id: int) -> CarInput:
    result = [car for car in db if car.id == id]
    if result:
        return result[0]
    else:
        raise HTTPException(status_code=404, detail=f"There is no car with id={id}.")


@app.post("/api/cars/", response_model=CarOutput)
def add_car(car: CarInput) -> CarOutput:
    new_car = CarOutput(size=car.size, doors=car.doors,
                        fuel=car.fuel, transmission=car.transmission,
                        id=len(db)+1)
    db.append(new_car)
    save_db(db)
    return new_car


if __name__ == "__main__":
    uvicorn.run("car_sharing:app", reload=True)
