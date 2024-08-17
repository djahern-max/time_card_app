from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, database

router = APIRouter()

@router.post("/timecards/daily", response_model=schemas.Timecard)
def create_daily_timecard(timecard: schemas.TimecardCreate, db: Session = Depends(database.get_db)):
    db_timecard = models.Timecard(**timecard.dict())
    db.add(db_timecard)
    db.commit()
    db.refresh(db_timecard)
    return db_timecard

@router.post("/timecards/mechanics", response_model=schemas.Timecard)
def create_mechanics_timecard(timecard: schemas.MechanicsTimecardCreate, db: Session = Depends(database.get_db)):
    db_timecard = models.Timecard(**timecard.dict())
    db.add(db_timecard)
    db.commit()
    db.refresh(db_timecard)
    return db_timecard

