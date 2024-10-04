#ocr.py is a FastAPI router that handles requests related to OCR (Optical Character Recognition).
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Form
from sqlalchemy.orm import Session
from app import models, database, oauth2
from app.database import get_db
from app.models import User
import logging

logger = logging.getLogger("uvicorn")

router = APIRouter()

# ... (other functions remain the same)

@router.get("/get_emp_code")
def get_emp_code(current_user: User = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):
    if current_user:
        return {"emp_code": current_user.emp_code}
    else:
        raise HTTPException(status_code=404, detail="User not found")

@router.get("/get_user_transactions")
def get_user_transactions(current_user: User = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):
    logger.info(f"Fetching transactions for user: {current_user.username}, Emp Code: {current_user.emp_code}")
    transactions = db.query(models.CreditCardTransaction).filter(models.CreditCardTransaction.emp_code == current_user.emp_code.strip()).all()
    logger.info(f"Found {len(transactions)} transactions")
    return transactions
