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
    guild = Column(Integer, unique=True)
    first_day = Column(Integer)
    current_day = Column(Integer)
    leap_year = Column(Boolean)
    # today = Column(String(80), nullable=True)


    def __init__(self, guild, first_day=546049, current_day=546049, leap_year=False):

        self.guild = int(guild)
        self.first_day = first_day
        self.current_day = current_day
        self.leap_year = leap_year

Base.metadata.create_all(engine)