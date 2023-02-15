from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.types import Date
from sqlalchemy.orm import relationship
from Database import Base


class Team(Base):
    __tablename__ = "Team"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    # country = Column(String(255), index=True)
    people = relationship("Person", lazy="joined")

class Person(Base):
    __tablename__ = "Person"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(255))
    last_name = Column(String(255))
    addresses = relationship("Address", lazy="joined")
    team_id = Column(Integer, ForeignKey("Team.id"))


class Address(Base):
    __tablename__ = "Address"

    id = Column(Integer, primary_key=True, index=True)
    line1 = Column(String(255))
    line2 = Column(String(255))
    city = Column(String(255))
    state = Column(String(255))
    zip = Column(Integer)
    person_id = Column(Integer, ForeignKey("Person.id"))

