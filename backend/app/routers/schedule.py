from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas
from app.database import get_db
from typing import List
from sqlalchemy import text
from datetime import timedelta, datetime

router = APIRouter()

@router.get("/schedule/{emp_code}", response_model=schemas.EmployeeSchedule)
def get_schedule(emp_code: str, db: Session = Depends(get_db)):
    try:
        query = text("""
            SELECT 
                t.emp_code,
                t.name,
                t.date,
                t.hours_worked,
                t.job,
                t.phase
            FROM timecards t
            WHERE 
                t.emp_code = :emp_code
            ORDER BY t.date ASC;
        """)
        results = db.execute(query, {'emp_code': emp_code}).fetchall()

        if not results:
            return {"emp_code": emp_code, "name": "", "jobs": []}

        schedule = {
            "emp_code": emp_code,
            "name": results[0].name,
            "jobs": []
        }

        # Group jobs by date
        jobs_by_date = {}
        for row in results:
            if row.date not in jobs_by_date:
                jobs_by_date[row.date] = []
            jobs_by_date[row.date].append({
                "job": row.job if row.job else None,
                "phase": row.phase if row.phase else None
            })

        for date, jobs in jobs_by_date.items():
            schedule["jobs"].append({
                "date": str(date),
                "jobs": jobs
            })

        return schedule
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/schedule", response_model=List[schemas.EmployeeSchedule])
def get_schedule(db: Session = Depends(get_db)):
    try:
        query = text("""
            SELECT 
                t.emp_code,
                t.name,
                t.date,
                t.job,
                t.phase
            FROM timecards t
            ORDER BY t.date ASC;
        """)
        results = db.execute(query).fetchall()

        schedule_list = [
            {
                "emp_code": row.emp_code,
                "name": row.name,
                "date": str(row.date),
                "jobs": [
                    {
                        "job": row.job,
                        "phase": row.phase
                    }
                ]
            }
            for row in results
        ]

        return schedule_list

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))