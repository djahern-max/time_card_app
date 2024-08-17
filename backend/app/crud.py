from sqlalchemy.orm import Session
from . import models, schemas
from .utils import hash_password

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(username=user.username, hashed_password=hash_password(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_timecard(db: Session, timecard: schemas.TimecardCreate, user_id: int):
    db_timecard = models.Timecard(**timecard.dict(), user_id=user_id)
    db.add(db_timecard)
    db.commit()
    db.refresh(db_timecard)
    return db_timecard

