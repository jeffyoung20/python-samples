from fastapi import FastAPI
import uvicorn

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# ***** Database Setup *****
SQLALCHEMY_DATABASE_URL = "sqlite:///one-file-db-server-db.sqlite"
# SQLALCHEMY_DATABASE_URL = "mysql://root:password@localhost:3306/test-db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Person(Base):
    __tablename__ = "Person"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(255))
    last_name = Column(String(255))

#Create DB Tables
Base.metadata.create_all(bind=engine)


# ***** web Server Config *****
app = FastAPI()
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

@app.get('/hello-world')
def helloWorld():
    return "Hello World"


@app.get('/person')
def getPerson():
    db =  SessionLocal()
    result = db.scalars(select(Person)).unique().all() 
    db.close()
    return result

@app.post('/person')
def addPerson(person: dict):
    db = SessionLocal()
    person = Person(first_name=person["first_name"], last_name=person["last_name"])
    db.add(person)
    db.commit()
    db.close()



uvicorn.run(app,host="127.0.0.1", port=8080)