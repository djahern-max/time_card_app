from sqlalchemy import Column, Integer, String, ForeignKey, Date, Boolean, Enum as SQLAEnum
from sqlalchemy.orm import relationship
from .database import Base
import enum

class UserRole(enum.Enum):
    mechanic = "mechanic"
    general = "general"
    admin = "admin"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    role = Column(SQLAEnum(UserRole), default=UserRole.general)

    mechanics_time_reports = relationship("MechanicsTimeReport", back_populates="user")
    daily_time_reports = relationship("DailyTimeReport", back_populates="user")

class MechanicsTimeReport(Base):
    __tablename__ = "mechanics_time_reports"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    date = Column(Date)
    hours_worked = Column(Integer)
    equipment = Column(String)
    equipment_number = Column(String)
    cost_category = Column(String)
    work_order_number = Column(String)
    description = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="mechanics_time_reports")

class DailyTimeReport(Base):
    __tablename__ = "daily_time_reports"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    date = Column(Date)
    hours_worked = Column(Integer)
    job_name = Column(String)
    description = Column(String)
    equipment = Column(String)
    loads = Column(String)
    pit = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="daily_time_reports")





