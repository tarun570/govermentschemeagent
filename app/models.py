from sqlalchemy import Column, Integer, String, Text
from .db import Base


class Scheme(Base):
    __tablename__ = "schemes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    eligibility = Column(Text)
    benefits = Column(Text)
