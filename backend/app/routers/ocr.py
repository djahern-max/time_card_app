import os
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Form
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app import models, database, oauth2
import pytesseract
from PIL import Image
from app.database import get_db
from app.models import User
from sqlalchemy.sql import func
import logging

logger = logging.getLogger("uvicorn")


router = APIRouter()

# Specify the directory where uploaded files will be stored
UPLOAD_DIRECTORY = r"C:\Users\dahern\Documents\ScheduleProjectUploads\Receipt_Images"

# Ensure the directory exists
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

@router.post("/upload_receipt")
async def upload_receipt(
    file: UploadFile = File(...),
    coding: str = Form(...),  # This can be the admin coding or any other type of coding
    employee_coding: str = Form(...),  # Accept employee coding information separately
    transaction_id: int = Form(...),  # Accept transaction_id from the frontend
    emp_code: str = Form(...),  # Accept employee code from the frontend
    db: Session = Depends(database.get_db),
    current_user: int = Depends(oauth2.get_current_user)
):
    try:
        # Save the file to the specified directory
        file_path = os.path.join(UPLOAD_DIRECTORY, file.filename)
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())

        # Use pytesseract to extract text from the image
        image = Image.open(file_path)
        text = pytesseract.image_to_string(image)

        # Save receipt information in the database
        receipt = models.Receipt(
            user_id=current_user.id,
            filename=file.filename,
            text=text,
            coding=coding,  # Store the admin or general coding information
            employee_coding=employee_coding,  # Store the employee coding information
            emp_code=emp_code,
            transaction_id=transaction_id,  # Store the transaction_id to link with the transaction
            image_path=file_path  # Store the file path in the receipt model
        )
        db.add(receipt)

        # Update the corresponding credit card transaction with employee coding and image path
        transaction = db.query(models.CreditCardTransaction).filter(models.CreditCardTransaction.id == transaction_id).first()
        if transaction:
            transaction.employee_coding = employee_coding
            transaction.image_path = file_path

        db.commit()
        db.refresh(receipt)

        return JSONResponse(content={"status": "success", "text": text, "image_path": file_path})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/get_emp_code")
def get_emp_code(current_user: int = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == current_user.id).first()
    if user:
        return {"emp_code": user.emp_code}
    else:
        raise HTTPException(status_code=404, detail="User not found")

@router.get("/get_user_transactions")
def get_user_transactions(current_user: User = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):
    print(f"Current User: {current_user.username}, Emp Code: {current_user.emp_code}")
    transactions = db.query(models.CreditCardTransaction).filter(models.CreditCardTransaction.emp_code == current_user.emp_code).all()
    return transactions

@router.get("/get_user_transactions")
def get_user_transactions(current_user: User = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):
    transactions = db.query(models.CreditCardTransaction).filter(models.CreditCardTransaction.emp_code == current_user.emp_code.strip()).all()
    return transactions

