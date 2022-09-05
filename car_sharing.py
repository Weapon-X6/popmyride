from typing import Optional

import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import create_engine, SQLModel, Session, select

from schemas import load_db, CarInput, save_db, CarOutput, TripOutput, TripInput, Car

app = FastAPI(title="Car Sharing")
db = load_db()

engine = create_engine("sqlite:///carsharing.db",
                       connect_args={"check_same_thread": False},
                       echo=True)


@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


@app.get("/api/cars")
def get_cars(size: Optional[str] = None, doors: Optional[int] = None, session: Session = Depends(get_session)) -> list:
    query = select(Car)
    if size:
        query = query.where(Car.size == size)
    if doors:
        query = query.where(Car.doors >= doors)
    return session.exec(query).all()


@app.get("/api/cars/{id}", response_model=Car)
def car_by_id(id: int, session: Session = Depends(get_session)) -> CarInput:
    car = session.get(Car, id)
    if car:
        return car
    else:
        raise HTTPException(status_code=404, detail=f"There is no car with id={id}.")


@app.post("/api/cars/", response_model=Car)
def add_car(car_input: CarInput, session: Session = Depends(get_session)) -> Car:
    new_car = Car.from_orm(car_input)
    session.add(new_car)
    session.commit()
    session.refresh(new_car)
    return new_car


@app.delete("/api/cars/{id}", status_code=204)
def remove_car(id: int, session: Session = Depends(get_session)) -> None:
    car = session.get(Car, id)
    if car:
        session.delete(car)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail=f"No car with id={id}.")


@app.put("/api/cars/{id}", response_model=Car)
def change_car(id: int, new_data: CarInput, session: Session = Depends(get_session)) -> CarOutput:
    car = session.get(Car, id)
    if car:
        car.fuel = new_data.fuel
        car.transmission = new_data.transmission
        car.size = new_data.size
        car.doors = new_data.doors
        session.commit()
        return car
    else:
        raise HTTPException(status_code=204, detail=f"No car with id={car_id}.")


@app.post("/api/cars/{car_id}/trips", response_model=TripOutput)
def add_trip(car_id: int, trip: TripInput) -> TripOutput:
    matches = [car for car in db if car.id == car_id]
    temp = id
    temp += 56
    if matches:
        car = matches[0]
        new_trip = TripOutput(id=len(car.trips)+1,
                              start=trip.start, end=trip.end,
                              description=trip.description)
        car.trips.append(new_trip)
        save_db(db)
        return new_trip
    else:
        raise HTTPException(status_code=404, detail=f"No car with id={id}")


if __name__ == "__main__":
    uvicorn.run("car_sharing:app", reload=True)
