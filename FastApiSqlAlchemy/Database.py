import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker



# ***** MySQL *****
# pip install mysqlclient
# SQLALCHEMY_DATABASE_URL = "mysql://root:password@localhost:3306/organization-db"

# ***** SQL Lite *****
SQLALCHEMY_DATABASE_URL = "sqlite:///organization-db.sqlite"

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=False)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

