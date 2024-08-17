from sqlalchemy.orm import Session
from app import models, schemas

def create_mechanics_timecard(db: Session, timecard: schemas.MechanicsTimecardCreate, user_id: int):
    db_timecard = models.MechanicsTimeReport(**timecard.dict(), user_id=user_id)
    db.add(db_timecard)
    db.commit()
    db.refresh(db_timecard)
    return db_timecard

def create_daily_timecard(db: Session, timecard: schemas.DailyTimecardCreate, user_id: int):
    db_timecard = models.DailyTimeReport(**timecard.dict(), user_id=user_id)
    db.add(db_timecard)
    db.commit()
    db.refresh(db_timecard)
    return db_timecard


