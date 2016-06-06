# coding: utf-8
from sqlalchemy import Column, Date, Integer, String, Table
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class Per(Base):
    __tablename__ = 'pers'

    id_persoon = Column(Integer, primary_key=True)
    prs_achternaam = Column(String(255))
    prs_tussenvoegsel = Column(String(45))
    prs_initialen = Column(String(255))
    prs_geboortedatum = Column(Date)
    type_vervoer = Column(String(255))
    naam_vervoer = Column(String(255))
    vertrek = Column(Date)
    aankomst = Column(Date)
    kaartenbak = Column(String(255))
    archieflink = Column(String(255))
    prs_uuid = Column(String(255))
    perscol = Column(String(45))


class TempReizen(Base):
    __tablename__ = 'temp_reizen'

    id = Column(Integer, primary_key=True)
    persoon = Column(Integer, nullable=False)
    vessel = Column(String(150))
    aankomst = Column(String(255))
    vertrek = Column(String(255))
    vessel_id = Column(Integer)


t_vervoer = Table(
    'vervoer', metadata,
    Column('type_vervoer', String(45)),
    Column('naam_vervoer', String(255)),
    Column('vertrek', Date),
    Column('aankomst', Date),
    Column('nummer', String(45))
)
