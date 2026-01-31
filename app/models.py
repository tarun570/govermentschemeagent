from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from .db import Base


class Scheme(Base):
    __tablename__ = "schemes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    eligibility = Column(Text)
    benefits = Column(Text)


# ------------------------
# Users table
# ------------------------
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    password = Column(String)

    businesses = relationship("BusinessProfile", back_populates="owner")


# ------------------------
# Business profiles table
# ------------------------
class BusinessProfile(Base):
    __tablename__ = "business_profiles"

    id = Column(Integer, primary_key=True, index=True)
    business_name = Column(String, nullable=False)
    description = Column(Text)

    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="businesses")




