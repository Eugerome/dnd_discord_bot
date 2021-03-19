"""Handle DB creation."""
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Date, Integer, String, Boolean, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from os import path

engine = create_engine("sqlite:///guilds.db", echo=True)
Session=sessionmaker(bind=engine)
session=Session()
Base = declarative_base()


class Guild(Base):

    __tablename__ = "server"

    id = Column(Integer, primary_key=True)
    guild = Column(String(50), unique=True)
    first_day = Column(Integer)
    current_day = Column(Integer)

    def __init__(self, guild, first_day=546048, current_day=546048):

        self.guild = guild
        self.first_day = first_day
        self.current_day = current_day    

Base.metadata.create_all(engine)