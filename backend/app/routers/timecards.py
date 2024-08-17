from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, models
from app.database import get_db

router = APIRouter()

@router.post("/timecards/mechanics", response_model=schemas.MechanicsTimeReport)
def create_mechanics_time_report(report: schemas.MechanicsTimecardCreate, db: Session = Depends(get_db)):
    db_report = models.MechanicsTimeReport(**report.dict())
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return db_report

@router.post("/timecards/daily", response_model=schemas.DailyTimeReport)
def create_daily_time_report(report: schemas.DailyTimecardCreate, db: Session = Depends(get_db)):
    db_report = models.DailyTimeReport(**report.dict())
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return db_report



