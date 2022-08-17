import json

from typing import Optional

from pydantic import BaseModel


class Car(BaseModel):
    id: int
    size: str
    fuel: Optional[str] = "electric"
    doors: int
    transmission: Optional[str] = "auto"


def load_db() -> list[Car]:
    """Load a list of Car objects from a JSOn file"""
    with open("cars.json") as f:
        return [Car.parse_obj(obj) for obj in json.load(f)]

