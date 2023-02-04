from typing import Optional

from sqlmodel import SQLModel, Field, Relationship


class TripInput(SQLModel):
    start: int
    end: int
    description: str


class TripOutput(TripInput):
    id: int


class Trip(TripInput, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    car_id: int = Field(foreign_key="car.id")
    car: "Car" = Relationship(back_populates="trips")


class CarInput(SQLModel):
    size: str
    fuel: Optional[str] = "electric"
    doors: int
    transmission: Optional[str] = "auto"

    class Config:
        schema_extra = {
            "example": {
                "size": "s",
                "doors": 5,
                "transmission": "manual",
                "fuel": "hybrid"
            }
        }


class Car(CarInput, table=True):
    id: Optional[int] = Field(primary_key=True, default=None)
    trips: list[Trip] = Relationship(back_populates="car")


class CarOutput(CarInput):
    id: int
    trips: list[TripOutput] = []



