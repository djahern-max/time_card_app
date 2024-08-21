from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum
from datetime import date
from typing import List


# Enum for User Roles
class UserRole(str, Enum):
    general = "general"
    mechanic = "mechanic"
    admin = "admin"

# User Schemas
class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str
    role: Optional[UserRole] = UserRole.general

class User(UserBase):
    id: int
    is_active: Optional[bool] = None
    role: UserRole

    class Config:
        from_attributes = True

# New class to include the access token in the response
class UserWithToken(User):
    access_token: str

    class Config:
        from_attributes = True

# Token schema
class Token(BaseModel):
    access_token: str
    token_type: str

# Base Schemas for Timecards
class TimecardBase(BaseModel):
    name: str
    date: datetime
    hours_worked: int

    class Config:
        from_attributes = True

# Mechanics Timecard Schemas
class MechanicsTimecardCreate(TimecardBase):
    equipment: str
    equipment_number: str
    cost_category: str
    work_order_number: str
    description: Optional[str] = None

    class Config:
        from_attributes = True

class MechanicsTimeReport(BaseModel):
    id: int
    name: str
    date: datetime
    hours_worked: int
    equipment: str
    equipment_number: str
    cost_category: str
    work_order_number: str
    description: Optional[str] = None

    class Config:
        from_attributes = True

# Daily Timecard Schemas
class DailyTimecardCreate(TimecardBase):
    job_name: str
    description: Optional[str] = None
    equipment: str
    loads: str
    pit: str

    class Config:
        from_attributes = True

class DailyTimeReport(BaseModel):
    id: int
    name: str
    date: datetime
    hours_worked: int
    job_name: str
    description: Optional[str] = None
    equipment: str
    loads: str
    pit: str

    class Config:
        from_attributes = True

# Equipment Schemas
class EquipmentBase(BaseModel):
    equipment_number: str
    equipment_name: str
    equipment_type: str
    

    class Config:
        from_attributes = True

class EquipmentCreate(EquipmentBase):
    pass

class Equipment(EquipmentBase):
    id: int

    class Config:
        from_attributes = True


class EmployeeBase(BaseModel):
    emp_code: str
    name: str
    street_address: Optional[str] = None
    town: Optional[str] = None
    zip: Optional[str] = None
    hire_date: Optional[date] = None
    marital_status: Optional[str] = None
    comp_code: Optional[str] = None
    general_department: Optional[str] = None
    department: Optional[str] = None
    department_code: Optional[str] = None
    phone_number: Optional[str] = None
    hourly_salary: Optional[float] = None
    pay_type_code: Optional[str] = None
    date_of_birth: Optional[date] = None
    title: Optional[str] = None
    pay_rate: Optional[float] = None
    username: Optional[str] = None
    password: Optional[str] = None
    role: Optional[str] = None

    class Config:
        from_attributes = True

# Schema for creating an employee (includes all fields)
class EmployeeCreate(EmployeeBase):
    pass

# Schema for returning an employee from the database (includes the ID)
class Employee(EmployeeBase):
    id: int

    class Config:
        from_attributes = True

# Base Schemas for Timecards
class TimecardBase(BaseModel):
    emp_code: str
    name: str
    date: date
    hours_worked: int
    rate: float
    extension: Optional[str] = None
    department: str
    job: str
    phase: str

    class Config:
        from_attributes = True

# Timecard Schemas
class TimecardCreate(TimecardBase):
    pass

class Timecard(TimecardBase):
    id: int

    class Config:
        from_attributes = True

class CombinedSchedule(BaseModel):
    date: str
    emp_code: str
    name: Optional[str] = None
    job: Optional[str] = None
    phase: Optional[str] = None
    card_last_four: str
    amount: float
    description: str

    class Config:
        orm_mode = True

from pydantic import BaseModel
from typing import Optional

class Schedule(BaseModel):
    emp_code: str
    date: str
    job: Optional[str] = None
    phase: Optional[str] = None

    class Config:
        orm_mode = True

class JobPhase(BaseModel):
    job: Optional[str] = None
    phase: Optional[str] = None

class JobWithDate(BaseModel):
    date: str
    jobs: List[JobPhase]

class EmployeeSchedule(BaseModel):
    emp_code: str
    name: str
    jobs: List[JobWithDate]

    class Config:
        from_attributes = True