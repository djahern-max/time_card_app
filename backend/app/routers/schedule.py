from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas
from app.database import get_db
from typing import List
from sqlalchemy import text

router = APIRouter()

@router.get("/schedule/{emp_code}/{date}", response_model=List[schemas.Schedule])
def get_employee_schedule(emp_code: str, date: str, db: Session = Depends(get_db)):
    try:
        schedule = db.execute(
            text(
                """
                SELECT
                    emp_code,
                    date,
                    job,
                    phase
                FROM
                    timecards
                WHERE
                    emp_code = :emp_code AND date = :date
                ORDER BY
                    date ASC;
                """
            ),
            {"emp_code": emp_code, "date": date}
        ).fetchall()

        schedule_list = [
            {
                "emp_code": row.emp_code,
                "date": row.date.strftime("%Y-%m-%d"),
                "job": row.job,
                "phase": row.phase
            }
            for row in schedule
        ]

        return schedule_list
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

