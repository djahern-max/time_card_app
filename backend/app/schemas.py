from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum

# Enum for User Roles
class UserRole(str, Enum):
    general = "general"
    mechanic = "mechanic"

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




