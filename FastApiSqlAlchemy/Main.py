from typing import List

import uvicorn

from fastapi import Depends, FastAPI, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

from sqlalchemy.orm import Session, joinedload
from sqlalchemy import text, select

import Models
import Schemas
from Database import SessionLocal, engine


Models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_methods=["*"],
#     allow_headers=["*"],
#     allow_credentials=True,
# )

# Dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.get("/")
def main():
    return RedirectResponse(url="/docs/")

@app.get("/test")
def Hello_world():
    return {"message": "hello world"}


@app.get("/person", response_model=List[Schemas.Person])
def get_all_people(db: Session = Depends(get_db)):
    # people = db.query(Models.Person).options(joinedload(Models.Person.addresses)).all()
    people = db.query(Models.Person).all()

    listRetPeople: List[Schemas.Person] = []
    # for pers in people:
    #     listAddr = []
    #     for addr in pers.addresses:
    #         listAddr.append( Schemas.Address(id=addr.id, line1=addr.line1))
    #     retPerson = Schemas.Person(id=pers.id,name=pers.name,addresses=listAddr)
    #     listRetPeople.append(retPerson)
    for persOrm in people:
        persDto: Schemas.Person = Schemas.Person.from_orm(persOrm)
        listRetPeople.append(persDto)
    return listRetPeople


@app.get("/person/{id}", response_model=Schemas.Person)
def get_person_by_id(id : int, db: Session = Depends(get_db)):
    personOrm = db.query(Models.Person).get(id)
    personDto: Schemas.Person = None
    if personOrm is not None:
        personDto = Schemas.Person.from_orm(personOrm)
    return personDto


# Query string example 
@app.get("/person", response_model=List[Schemas.Person])
def get_person_by_id(lname : str, fname: str, db: Session = Depends(get_db)):
    # people = db.query(Models.Person).where(text(f"name == '{name}'"))
    # people = db.execute(select(Models.Person).where(Models.Person.name == name)).scalars().unique()
    people: List[Models.Person] = db.scalars(select(Models.Person)
        .where(Models.Person.last_name.upper() == lname.upper() and Models.Person.first_name.upper() == fname.upper())).unique(strategy=None).all()
    listRetPeople: List[Schemas.Person] = []
    for persOrm in people:
        personDto: Schemas.Person = Schemas.Person.from_orm(persOrm)
        listRetPeople.append(personDto)
    return listRetPeople



@app.post("/person", response_model=Schemas.Person)
def add_person(personDto: Schemas.Person, db: Session = Depends(get_db)):
    # newPersonOrm = Models.Person(first_name=personDto.first_name, last_name=personDto.last_name)
    # for addrDto in personDto.addresses:
    #     newAddrOrm = Models.Address(line1=addrDto.line1, line2=addrDto.line2, city=addrDto.city, zip=addrDto.zip)
    #     newPersonOrm.addresses.append(newAddrOrm)
    newPersonOrm: Models.Person = createPersonOrm(personDto)
    db.add(newPersonOrm)
    db.commit()
    personOrm = db.query(Models.Person).get(newPersonOrm.id)
    personDto: Schemas.Person = Schemas.Person.from_orm(personOrm)
    return personDto 


@app.delete("/person/{id}")
def delete_person_by_id(id : int, db: Session = Depends(get_db)):
    userOrm = db.query(Models.Person).get(id)
    if userOrm != None:
        db.delete(userOrm)
        db.commit()



#*************** TEAMS ***************
@app.get("/team", response_model=List[Schemas.Team])
def get_all_teams(db: Session = Depends(get_db)):
    listTeamsOrm: Models.Team = db.query(Models.Team).all()
    listRetTeams: List[Schemas.Teams] = []
    for teamOrm in listTeamsOrm:
        teamDto: Schemas.Team = Schemas.Team.from_orm(teamOrm)
        listRetTeams.append(teamDto)
    return listRetTeams

@app.post("/team", response_model=Schemas.Team)
def add_person(teamDto: Schemas.Team, db: Session = Depends(get_db)):
    newTeamOrm: Models.Team = Models.Team(name=teamDto.name)
    for personDto in teamDto.people:
        if type(personDto) != int:
            newPersonOrm: Models.Person = createPersonOrm(personDto)
            newTeamOrm.people.append(newPersonOrm)
        else:
            personToAddOrm: Models.Person = db.scalars(select(Models.Person).where(Models.Person.id == personDto)).first()
            if personToAddOrm != None:
                newTeamOrm.people.append(personToAddOrm)
    db.add(newTeamOrm)
    db.commit()
    teamOrm = db.query(Models.Team).get(newTeamOrm.id)
    teamDto: Schemas.Team = Schemas.Team.from_orm(teamOrm)
    return newTeamOrm 

@app.delete("/team/{id}")
def delete_team_by_id(id : int, db: Session = Depends(get_db)):
    teamOrm = db.query(Models.Team).get(id)
    if teamOrm != None:
        db.delete(teamOrm)
        db.commit()


#*************** Helper Funcs ***************
def createPersonOrm(personDto: Schemas.Person):
    newPersonOrm = Models.Person(first_name=personDto.first_name, last_name=personDto.last_name)
    for addrDto in personDto.addresses:
        newAddrOrm = Models.Address(line1=addrDto.line1, line2=addrDto.line2, city=addrDto.city, zip=addrDto.zip)
        newPersonOrm.addresses.append(newAddrOrm)
    return newPersonOrm


# Direct to Database
@app.get("/person-db/")
def get_all_people_2(db: Session = Depends(get_db)):
    # people = db.query(Models.Person).options(joinedload(Models.Person.addresses)).all()
    listPeople = db.query(Models.Person).all()
    return listPeople

# Direct to Database
@app.get("/person-db/{id}")
def get_person_by_id_2(id : int, db: Session = Depends(get_db)):
    person = db.query(Models.Person).get(id)
    return person




if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)