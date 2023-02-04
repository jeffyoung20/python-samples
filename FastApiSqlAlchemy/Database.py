import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# SQLALCHEMY_DATABASE_URL = os.getenv("DB_CONN")
# SQLALCHEMY_DATABASE_URL = "mysql://uname:password@url:3306/FastApiPoc"
SQLALCHEMY_DATABASE_URL = "sqlite:///jeff-test.sqlite"

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=False)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

