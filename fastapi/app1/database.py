from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base


SQLALCHEMY_DATABASE_URL='postgresql://postgres:1234@localhost/dbs'
Base=declarative_base()

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
