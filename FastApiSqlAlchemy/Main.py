from typing import List

import uvicorn

from fastapi import Depends, FastAPI, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

from sqlalchemy.orm import Session, joinedload
from sqlalchemy import text, select, func

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



#*************** PERSON ***************
@app.get("/person", response_model=List[Schemas.Person])
def get_all_people(db: Session = Depends(get_db)):
    # people = db.query(Models.Person).options(joinedload(Models.Person.addresses)).all()
    people = db.scalars(select(Models.Person)).unique().all()

    listRetPeople: List[Schemas.Person] = []
    for persOrm in people:
        persDto: Schemas.Person = Schemas.Person.from_orm(persOrm)
        listRetPeople.append(persDto)
    return listRetPeople


@app.get("/person/{id}", response_model=Schemas.Person)
def get_person_by_id(id : int, db: Session = Depends(get_db)):
    personOrm = db.scalars(select(Models.Person).where(Models.Person.id == id)).unique().first()
    personDto: Schemas.Person = None
    if personOrm is not None:
        personDto = Schemas.Person.from_orm(personOrm)
    return personDto


# Query string example 
@app.get("/person/", response_model=List[Schemas.Person])
def get_person_by_fname_lname(lname : str, fname: str, db: Session = Depends(get_db)):
    people: List[Models.Person] = db.scalars(select(Models.Person) 
        .where(func.upper(Models.Person.last_name) == lname.upper() \
            and func.upper(Models.Person.first_name) == fname.upper())) \
        .unique(strategy=None).all()
    listRetPeople: List[Schemas.Person] = []
    for persOrm in people:
        personDto: Schemas.Person = Schemas.Person.from_orm(persOrm)
        listRetPeople.append(personDto)
    return listRetPeople



@app.post("/person", response_model=List[Schemas.Person])
def add_person(personDtoList: List[Schemas.Person], db: Session = Depends(get_db)):
    personDtoListOut: List[Schemas.Person] = []
    for personDto in personDtoList:
        newPersonOrm: Models.Person = createPersonOrm(personDto)
        db.add(newPersonOrm)
        db.commit()
        personOrm = db.query(Models.Person).get(newPersonOrm.id)
        personDto: Schemas.Person = Schemas.Person.from_orm(personOrm)
        personDtoListOut.append(personDto)
    return personDtoListOut 


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

@app.post("/team", response_model=List[Schemas.Team])
def add_person(teamsListDto: List[Schemas.Team], db: Session = Depends(get_db)):
    teamsListDtoOut: List[Schemas.Team] = []
    for teamDto in teamsListDto:
        insertTeam: bool = False
        teamOrm: Schemas.Team = db.scalars(select(Models.Team).where(func.upper(Models.Team.name) == teamDto.name.upper())).first()
        if teamOrm == None:
            teamOrm: Models.Team = Models.Team(name=teamDto.name)
            insertTeam = True
        else:
            teamOrm.people = []
        for personDto in teamDto.people:
            if hasattr(personDto,"person_id") :
                personToAddOrm: Models.Person = db.scalars(select(Models.Person).where(Models.Person.id == personDto.person_id)).first()
                if personToAddOrm != None:
                    teamOrm.people.append(personToAddOrm)
            else:
                personToAddOrm: Models.Person = db.scalars(select(Models.Person)
                    .where(func.upper(Models.Person.first_name) == personDto.first_name.upper() \
                        and func.upper(Models.Person.last_name) == personDto.last_name.upper())) \
                    .first()
                if personToAddOrm != None:
                    personToAddOrm.addresses.clear()
                    for addressDto in personDto.addresses:
                        addressToAddOrm: Models.Address = \
                            Models.Address(line1=addressDto.line1, line2=addressDto.line2, city=addressDto.city, \
                                state=addressDto.state, zip=addressDto.zip)
                        # db.add(addressToAddOrm)
                        personToAddOrm.addresses.append(addressToAddOrm)
                else:
                    personToAddOrm = createPersonOrm(personDto)
                teamOrm.people.append(personToAddOrm)
        if insertTeam:
            db.add(teamOrm)
        db.commit()
        teamOrmRet = db.scalars(select(Models.Team).where(Models.Team.id == teamOrm.id)).first()
        teamDtoReturn: Schemas.Team = Schemas.Team.from_orm(teamOrmRet)
        teamsListDtoOut.append(teamDtoReturn)
    return teamsListDtoOut


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