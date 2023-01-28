from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.types import Date
from sqlalchemy.orm import relationship
from Database import Base


class Person(Base):
    __tablename__ = "Person"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    # country = Column(String(255), index=True)
    addresses = relationship("Address", lazy="joined")

class Address(Base):
    __tablename__ = "Address"

    id = Column(Integer, primary_key=True, index=True)
    line1 = Column(String(255))
    person_id = Column(Integer, ForeignKey("Person.id"))
    bricks = relationship("Brick", lazy="joined")

class Brick(Base):
    __tablename__ = "Brick"
    id = Column(Integer, primary_key=True, index=True)
    brick_value = Column(String(255))
    address_id = Column(Integer, ForeignKey("Address.id"))
    type = Column(Integer)


# Move to other dev teams
# class XPerson(Person):
#     surname = Column(String(256))
