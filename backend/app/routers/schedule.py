# schedule.py will contain the route for getting the schedule of an employee.
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas
from app.database import get_db
from typing import List
from sqlalchemy import text


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
                t.rate,
                t.job,
                t.phase
            FROM timecards t
            WHERE 
                TRIM(UPPER(t.emp_code)) = TRIM(UPPER(:emp_code))
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

        jobs_by_date = {}
        for row in results:
            if row.date not in jobs_by_date:
                jobs_by_date[row.date] = []
            jobs_by_date[row.date].append({
                "job": row.job if row.job else "Unknown",
                "phase": row.phase if row.phase else "Unknown",
                "hours_worked": row.hours_worked if row.hours_worked is not None else None,
                "rate": row.rate if row.rate is not None else None
            })

        for date, jobs in jobs_by_date.items():
            schedule["jobs"].append({
                "date": str(date),
                "jobs": jobs
            })

        return schedule
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    
