"""Handle DB creation."""
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String, Boolean, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from os import path

engine = create_engine(f'sqlite:///{path.dirname(path.realpath(__file__))}\\data\\instances.db', echo=True)
Base = declarative_base()


class Server(Base):

    __tablename__ = "server"

    id = Column(Integer, primary_key=True)
    guid = Column(String(50), unique=True)
    first_day = Column(Integer)
    current_day = Column(Integer)

Base.metadata.create_all(engine)