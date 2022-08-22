import json

from typing import Optional

from pydantic import BaseModel


class CarInput(BaseModel):
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


class CarOutput(CarInput):
    id: int


def load_db() -> list[CarOutput]:
    """Load a list of Car objects from a JSOn file"""
    with open("cars.json") as f:
        return [CarOutput.parse_obj(obj) for obj in json.load(f)]


def save_db(cars: list[CarOutput]):
    with open("cars.json", "w") as f:
        json.dump([car.dict() for car in cars], f, indent=4)
