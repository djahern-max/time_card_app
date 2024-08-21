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

class JobPhase(Base):
    __tablename__ = "job_phases"

    id = Column(Integer, primary_key=True, index=True)
    job = Column(String, index=True, nullable=False)
    phase_number = Column(String, index=True, nullable=False)
    phase_name = Column(String, nullable=True)
    cost_type = Column(String, nullable=True)

# Equipment Model
class Equipment(Base):
    __tablename__ = "equipment"

    id = Column(Integer, primary_key=True, index=True)
    equipment_number = Column(String, nullable=False)
    equipment_name = Column(String, nullable=False)
    equipment_type = Column(String, nullable=False)



class Employee(Base):
    __tablename__ = "employees"

    emp_code = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    street_address = Column(String, nullable=False)
    town = Column(String, nullable=False)
    zip = Column(String, nullable=False)
    hire_date = Column(Date, nullable=False)
    marital_status = Column(String, nullable=False)
    comp_code = Column(String, nullable=False)
    general_department = Column(String, nullable=False)
    department = Column(String, nullable=False)
    department_code = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    hourly_salary = Column(String, nullable=False)
    pay_type_code = Column(String, nullable=False)
    date_of_birth = Column(Date, nullable=False)
    title = Column(String, nullable=False)
    pay_rate = Column(String, nullable=False)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)

# Timecard Model
class Timecard(Base):
    __tablename__ = "timecards"

    id = Column(Integer, primary_key=True, index=True)
    emp_code = Column(String, nullable=False)
    name = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    hours_worked = Column(Integer, nullable=False)
    rate = Column(String, nullable=False)
    extension = Column(String, nullable=True)
    department = Column(String, nullable=False)
    job = Column(String, nullable=False)
    phase = Column(String, nullable=False)

