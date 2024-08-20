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
                WITH timecard_cte AS (
                    SELECT 
                        t.emp_code, 
                        t.date, 
                        t.name, 
                        t.job, 
                        t.phase, 
                        ROW_NUMBER() OVER (PARTITION BY t.emp_code ORDER BY t.date DESC) AS rn
                    FROM 
                        timecards t
                    JOIN 
                        credit_card_transactions c 
                    ON 
                        t.emp_code = c.emp_code
                    WHERE
                        t.date BETWEEN (c.transaction_date - INTERVAL '2 DAY') AND c.transaction_date
                )
                SELECT
                    c.transaction_date AS date,
                    c.emp_code,
                    COALESCE(t.name, '') AS name,
                    COALESCE(t.job, '') AS job,
                    COALESCE(t.phase, '') AS phase,
                    c.card_last_four,
                    c.amount,
                    c.description
                FROM
                    credit_card_transactions c
                LEFT JOIN 
                    timecard_cte t 
                ON 
                    c.emp_code = t.emp_code 
                ORDER BY
                    c.transaction_date ASC;
                """
            )
        ).fetchall()

        combined_schedule_list = [
            {
                "date": row[0].strftime("%Y-%m-%d"),  # Convert to string in "YYYY-MM-DD" format
                "emp_code": row[1],
                "name": row[2],
                "job": row[3],
                "phase": row[4],
                "card_last_four": row[5],
                "amount": row[6],
                "description": row[7]
            } for row in combined_schedule
        ]

        return combined_schedule_list
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



