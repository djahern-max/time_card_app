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
    role: Optional[UserRole] = UserRole.general  # Optional role with a default value

class User(UserBase):
    id: int
    is_active: Optional[bool] = None
    role: UserRole  # Role field to store the user's role

    class Config:
        from_attributes = True

# New class to include the access token in the response
class UserWithToken(User):
    access_token: str

# Timecard Schemas
class TimecardBase(BaseModel):
    hours_worked: int
    job_name: str
    description: Optional[str] = None
    equipment_used: Optional[str] = None

class TimecardCreate(TimecardBase):
    pass

class Timecard(TimecardBase):
    id: int
    date: datetime = datetime.utcnow()
    user_id: int

    class Config:
        from_attributes = True

# Mechanics Timecard Schema
class MechanicsTimecardCreate(TimecardBase):
    additional_mechanic_field: Optional[str] = None  # Example additional field for mechanics

    class Config:
        from_attributes = True

# Token schema
class Token(BaseModel):
    access_token: str
    token_type: str







