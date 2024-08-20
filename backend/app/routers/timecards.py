from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, models
from app.database import get_db
from typing import List
from sqlalchemy import text

router = APIRouter()

@router.post("/timecards/mechanics", response_model=schemas.MechanicsTimeReport)
def create_mechanics_time_report(report: schemas.MechanicsTimecardCreate, db: Session = Depends(get_db)):
    db_report = models.MechanicsTimeReport(**report.dict())
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return db_report

@router.post("/timecards/general", response_model=schemas.DailyTimeReport)
def create_daily_time_report(report: schemas.DailyTimecardCreate, db: Session = Depends(get_db)):
    db_report = models.DailyTimeReport(**report.dict())
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return db_report



@router.get("/combined", response_model=List[schemas.CombinedSchedule])
def get_combined_schedule(db: Session = Depends(get_db)):
    try:
        combined_schedule = db.execute(
            text(
                """
                SELECT
                    t.date,
                    t.name,
                    t.job,
                    t.phase,
                    c.card_last_four,
                    c.amount,
                    c.description
                FROM
                    timecards t
                JOIN
                    credit_card_transactions c
                ON
                    t.emp_code = c.emp_code
                    AND t.date = c.transaction_date
                ORDER BY
                    t.date ASC;
                """
            )
        ).fetchall()

        combined_schedule_list = [
            {
                "date": row[0],
                "name": row[1],
                "job": row[2],
                "phase": row[3],
                "card_last_four": row[4],
                "amount": row[5],
                "description": row[6]
            } for row in combined_schedule
        ]

        return combined_schedule_list
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))