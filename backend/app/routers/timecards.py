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



@router.get("/credit_card_transactions", response_model=List[schemas.CombinedSchedule])
def get_credit_card_transactions(db: Session = Depends(get_db)):
    try:
        transactions = db.execute(
            text(
                """
                SELECT
                    c.transaction_date AS date,
                    c.emp_code,
                    c.card_last_four,
                    c.amount,
                    c.description
                FROM
                    credit_card_transactions c
                ORDER BY
                    c.transaction_date ASC;
                """
            )
        ).fetchall()

        transactions_list = [
            {
                "date": row.date.strftime("%Y-%m-%d"),
                "emp_code": row.emp_code,
                "card_last_four": row.card_last_four,
                "amount": row.amount,
                "description": row.description
            }
            for row in transactions
        ]

        return transactions_list
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

