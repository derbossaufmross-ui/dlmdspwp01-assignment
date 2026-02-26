"""
Database models for DLMDSPWP01 project.
Defines all required tables according to the requirements."""

from sqlalchemy import create_engine, Column, Integer, Float
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class TrainingData(Base):
    """Table for the four training functions"""
    __tablename__ = "training_data"

    x = Column(Float, primary_key=True)
    y1 = Column(Float)
    y2 = Column(Float)
    y3 = Column(Float)
    y4 = Column(Float)


class IdealFunctions(Base):
    """Table for the 50 ideal functions"""
    __tablename__ = "ideal_functions"

    x = Column(Float, primary_key=True)


for i in range(1, 51):
    setattr(IdealFunctions, f"y{i}", Column(Float))


class TestMapping(Base):
    """Table storing accepted test points with deviation and chosen ideal function number."""

    __tablename__ = "test_mapping"

    x = Column(Float, primary_key=True)
    y = Column(Float, primary_key=True)

    delta_y = Column(Float, nullable=False)
    ideal_no = Column(Integer, nullable=False)


def create_database(db_path: str = "database/project.db"):
    """Create SQLite database file and all tables."""
    engine = create_engine(f"sqlite:///{db_path}")
    Base.metadata.create_all(engine)
    return engine


