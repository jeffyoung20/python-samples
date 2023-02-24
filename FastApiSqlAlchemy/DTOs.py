from datetime import date
from typing import List, Optional
from pydantic import BaseModel


class Address(BaseModel):
    id: Optional[int]
    line1: str
    line2: Optional[str]
    city: Optional[str]
    state: Optional[str]
    zip: Optional[int]
    class Config:
        orm_mode = True

class Person(BaseModel):
    id: Optional[int]
    first_name: str
    last_name: str
    addresses: Optional[List[Address]] =[]
    class Config:
        orm_mode = True

class PersonRef(BaseModel):
    person_id: int
    class Config:
        orm_mode = True

class Team(BaseModel):
    id: Optional[int]
    name: str
    people: Optional[List[Person | PersonRef] ] = []
    # people_ids: Optional[List[int]] = []
    class Config:
        orm_mode = True

