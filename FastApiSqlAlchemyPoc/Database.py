import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# SQLALCHEMY_DATABASE_URL = os.getenv("DB_CONN")
# SQLALCHEMY_DATABASE_URL = "mysql://admin:***REMOVED***@MDM_CONFIG.mysql-poc.cle7vfprs9ue.us-east-1.rds.amazonaws.com:3306/MDM_CONFIG"
SQLALCHEMY_DATABASE_URL = "sqlite:///jeff-test.sqlite"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

