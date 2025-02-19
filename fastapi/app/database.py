from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL='postgresql://postgres:1234@localhost/fastapi'

engine=create_engine(SQLALCHEMY_DATABASE_URL)

sessionLocal=sessionmaker(autoflush=False,autocommit=False,bind=engine)


Base=declarative_base()


def get_db():
    db=sessionLocal()
    try:
        yield db
    finally:
        db.close()
