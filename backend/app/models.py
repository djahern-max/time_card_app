from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Enum as SQLAEnum
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime
import enum

class UserRole(enum.Enum):
    mechanic = "mechanic"
    general = "general"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    role = Column(SQLAEnum(UserRole), default=UserRole.general)  # Correct usage of SQLAEnum

    timecards = relationship("Timecard", back_populates="user")

class Timecard(Base):
    __tablename__ = "timecards"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, default=datetime.utcnow)
    hours_worked = Column(Integer, nullable=False)
    job_name = Column(String, nullable=False)
    description = Column(String)
    equipment_used = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="timecards")


