from flask import config
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgresql://postgres:password@127.0.0.1:5432/invest')
_SessionFactory = sessionmaker(bind=engine)
Base = declarative_base()

def session_factory():
    Base.metadata.create_all(engine)
    return _SessionFactory()