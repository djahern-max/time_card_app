from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# User Schemas
class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: Optional[bool] = None  # Made optional to avoid issues if not provided in the response

    class Config:
        from_attributes = True

# New class to include the access token in the response
class UserWithToken(User):
    access_token: str

# Token Schema for login response
class Token(BaseModel):
    access_token: str
    token_type: str

# Login Schema
class Login(BaseModel):
    username: str
    password: str

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





