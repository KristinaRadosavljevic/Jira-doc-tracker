from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class ReleaseNumber(Base):
    __tablename__ = "release_number"

    rn = Column(String, primary_key=True)