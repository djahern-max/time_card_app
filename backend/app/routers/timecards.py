from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud, models
from app.database import get_db
from app.oauth2 import get_current_user  # Assuming you have an oauth2 file for authentication

router = APIRouter()

@router.post("/timecards/", response_model=schemas.Timecard)
def create_timecard(
    timecard: schemas.TimecardCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # Pass the current user's ID to the create_timecard function
    return crud.create_timecard(db=db, timecard=timecard, user_id=current_user.id)
