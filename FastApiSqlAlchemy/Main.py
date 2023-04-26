from typing import List

import uvicorn

from fastapi import Depends, FastAPI, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

from sqlalchemy.orm import Session, joinedload
from sqlalchemy import text, select, func

import FastApiSqlAlchemy.Models as Models
import FastApiSqlAlchemy.DTOs as DTOs
from FastApiSqlAlchemy.Database import SessionLocal, engine


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
@app.get("/person", response_model=List[DTOs.Person])
# @app.get("/person")
def get_all_people(db: Session = Depends(get_db)):
    people = getPersonAll(db)

    listRetPeople: List[DTOs.Person] = []
    for persOrm in people:
        persDto: DTOs.Person = DTOs.Person.from_orm(persOrm)
        listRetPeople.append(persDto)
    return listRetPeople


@app.get("/person/{id}", response_model=DTOs.Person)
def get_person_by_id(id : int, db: Session = Depends(get_db)):
    personOrm: Models.Person = getPersonById(db, id)
    personDto: DTOs.Person = None
    if personOrm is not None:
        personDto = DTOs.Person.from_orm(personOrm)
    return personDto


# Query string example 
@app.get("/person/", response_model=DTOs.Person)
def get_person_by_fname_lname(lname : str, fname: str, db: Session = Depends(get_db)):
    persOrm: Models.Person = getPersonByLNameFName(db, lname, fname)
    return DTOs.Person.from_orm(persOrm)



@app.post("/person", response_model=List[DTOs.Person])
def add_person(personDtoList: List[DTOs.Person], db: Session = Depends(get_db)):
    personDtoListOut: List[DTOs.Person] = []
    for personDto in personDtoList:
        personToUpdateOrm: Models.Person = getPersonByLNameFName(db, personDto.last_name, personDto.first_name) 
        if personToUpdateOrm == None:
            personToUpdateOrm = createPersonOrm(personDto)
            db.add(personToUpdateOrm)
        else:
            updatePersonOrm(personDto, personToUpdateOrm)
        db.commit()
        # personOrm = db.query(Models.Person).get(personToUpdateOrm.id)
        personOrm = getPersonById(db, personToUpdateOrm.id)
        personDto: DTOs.Person = DTOs.Person.from_orm(personOrm)
        personDtoListOut.append(personDto)
    return personDtoListOut 


@app.delete("/person/{id}")
def delete_person_by_id(id : int, db: Session = Depends(get_db)):
    personOrm: Models.Person = getPersonById(db, id)
    if personOrm != None:
        db.delete(personOrm)
        db.commit()



#*************** TEAMS ***************
@app.get("/team", response_model=List[DTOs.Team])
def get_all_teams(db: Session = Depends(get_db)):
    listTeamsOrm: List[Models.Team] = getAllTeams(db)
    listRetTeams: List[DTOs.Teams] = []
    for teamOrm in listTeamsOrm:
        teamDto: DTOs.Team = DTOs.Team.from_orm(teamOrm)
        listRetTeams.append(teamDto)
    return listRetTeams

@app.get("/team/{id}", response_model=DTOs.Team)
def get_team_by_id(id : int, db: Session = Depends(get_db)):
    teamOrm: Models.Team = getTeamById(db, id)
    teamDto: DTOs.Person = None
    if teamOrm is not None:
        teamDto = DTOs.Team.from_orm(teamOrm)
    return teamDto

@app.post("/team", response_model=List[DTOs.Team])
def add_teams(teamsListDto: List[DTOs.Team], db: Session = Depends(get_db)):
    teamsListDtoOut: List[DTOs.Team] = []
    for teamDto in teamsListDto:
        teamOrm: Models.Team = getTeamByName(db, teamDto.name)
        if teamOrm == None:
            teamOrm: Models.Team = Models.Team(name=teamDto.name)
            db.add(teamOrm)
        else:
            teamOrm.people = []
        for personDto in teamDto.people:
            if hasattr(personDto,"person_id") :
                # ********** Reference ID *********
                personToAddOrm: Models.Person = getPersonById(db, personDto.person_id)
                if personToAddOrm != None:
                    teamOrm.people.append(personToAddOrm)
            else:
                personToAddOrm: Models.Person = getPersonByLNameFName(db, personDto.last_name, personDto.first_name) 
                if personToAddOrm == None:
                    # ********** Add Person *********
                    personToAddOrm = createPersonOrm(personDto)
                    teamOrm.people.append(personToAddOrm)
                else:
                    # ********** Update Existing Person *********
                    updatePersonOrm(personDto, personToAddOrm)
                    teamOrm.people.append(personToAddOrm)
        db.commit()
        teamOrmRet = db.scalars(select(Models.Team).where(Models.Team.id == teamOrm.id)).first()
        teamDtoReturn: DTOs.Team = DTOs.Team.from_orm(teamOrmRet)
        teamsListDtoOut.append(teamDtoReturn)
    return teamsListDtoOut


@app.delete("/team/{id}")
def delete_team_by_id(id : int, db: Session = Depends(get_db)):
    teamOrm = db.query(Models.Team).get(id)
    if teamOrm != None:
        db.delete(teamOrm)
        db.commit()


#*************** Database Helper Funcs ***************
def getPersonAll(db: Session) -> List[Models.Person]:
    # people = db.query(Models.Person).options(joinedload(Models.Person.addresses)).all()
    return db.scalars(getPersonStmt() ).unique().all()

def getPersonById(db: Session, id: int) -> Models.Person:
    return db.scalars(getPersonStmt().where(Models.Person.id == id)).unique().first()

def getPersonByLNameFName(db: Session, lastName: str, firstName: str) -> Models.Person:
    personOrm: Models.Person = db.scalars(getPersonStmt()
        .filter(func.upper(Models.Person.first_name) == firstName.upper()) \
        .filter(func.upper(Models.Person.last_name) == lastName.upper())) \
        .first()
    return personOrm

def getPersonStmt():
    stmt = select(Models.Person).options( joinedload(Models.Person.addresses))
    # stmt = select(Models.Person, Models.Address).join(Models.Address)
    return stmt


def getAllTeams(db: Session ) -> List[Models.Team]:
    return  db.scalars(geTeamsStmt()).unique().all() 

def getTeamById(db: Session, id: int) -> Models.Team:
    return db.scalars(geTeamsStmt().where(Models.Team.id == id)).unique().first()

def getTeamByName(db: Session, teamName: str) -> Models.Team:
    return db.scalars(geTeamsStmt().where(func.upper(Models.Team.name) == teamName.upper())).first()

def geTeamsStmt():
    stmt = select(Models.Team).options( joinedload(Models.Team.people).joinedload(Models.Person.addresses))
    return stmt


#*************** Helper Funcs ***************
def createPersonOrm(personDto: DTOs.Person):
    newPersonOrm = Models.Person(first_name=personDto.first_name, last_name=personDto.last_name)
    for addrDto in personDto.addresses:
        newAddrOrm = Models.Address(line1=addrDto.line1, line2=addrDto.line2, city=addrDto.city, \
            state=addrDto.state, zip=addrDto.zip)
        newPersonOrm.addresses.append(newAddrOrm)
    return newPersonOrm

def updatePersonOrm(personDto: DTOs.Person, personToUpdateOrm: Models.Person ):
    personToUpdateOrm.addresses.clear()
    for addressDto in personDto.addresses:
        addressToAddOrm: Models.Address = \
            Models.Address(line1=addressDto.line1, line2=addressDto.line2, city=addressDto.city, \
                state=addressDto.state, zip=addressDto.zip)
        personToUpdateOrm.addresses.append(addressToAddOrm)


# Direct to Database
# @app.get("/person-db/")
# def get_all_people_2(db: Session = Depends(get_db)):
#     # people = db.query(Models.Person).options(joinedload(Models.Person.addresses)).all()
#     listPeople = db.query(Models.Person).all()
#     return listPeople

# # Direct to Database
# @app.get("/person-db/{id}")
# def get_person_by_id_2(id : int, db: Session = Depends(get_db)):
#     person = db.query(Models.Person).get(id)
#     return person




if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)