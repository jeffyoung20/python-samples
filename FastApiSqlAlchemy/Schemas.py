from datetime import date
from typing import List, Optional
from pydantic import BaseModel


class Brick(BaseModel):
    id: int
    brick_value: str
    type: int
    class Config:
        orm_mode = True

class Address(BaseModel):
    id: int
    line1: str
    bricks: Optional[List[Brick]]
    class Config:
        orm_mode = True

class Person(BaseModel):
    id: int
    name: str
    addresses: Optional[List[Address]]

    class Config:
        orm_mode = True


