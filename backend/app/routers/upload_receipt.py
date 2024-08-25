import os
import logging
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from PIL import Image
import pytesseract
from . import models, oauth2
from app.database import get_db


# Configure logging
logging.basicConfig(level=logging.INFO)

router = APIRouter()

UPLOAD_DIRECTORY = "C:/Users/dahern/Documents/ScheduleProjectUploads/Receipt Images"

import os
import logging
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from PIL import Image
import pytesseract
from . import models, oauth2
from .database import get_db

# Configure logging
logging.basicConfig(level=logging.INFO)

router = APIRouter()

UPLOAD_DIRECTORY = "C:/Users/dahern/Documents/ScheduleProjectUploads/Receipt Images"

@router.post("/upload_receipt")
async def upload_receipt(
    file: UploadFile = File(...),
    coding: str = Form(...),
    transaction_id: int = Form(...),
    emp_code: str = Form(...),
    employee_coding: str = Form(...),
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)
):
    try:
        logging.info("Starting receipt upload process.")

        # Save the file to the specified directory
        file_path = os.path.join(UPLOAD_DIRECTORY, file.filename)
        logging.info(f"Saving file to: {file_path}")
        
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())

        logging.info("File saved successfully.")

        # Use pytesseract to extract text from the image
        image = Image.open(file_path)
        text = pytesseract.image_to_string(image)

        logging.info(f"OCR Text extracted: {text}")

        # Save receipt information in the database
        receipt = models.Receipt(
            user_id=current_user.id,
            filename=file.filename,
            text=text,
            coding=coding,
            emp_code=emp_code,
            transaction_id=transaction_id,
            image_path=file_path
        )
        db.add(receipt)

        # Update the corresponding credit card transaction with employee coding and image path
        transaction = db.query(models.CreditCardTransaction).filter(models.CreditCardTransaction.id == transaction_id).first()
        if transaction:  # Correct indentation
            logging.info(f"Updating transaction {transaction_id} with coding and image path.")
            transaction.employee_coding = employee_coding
            transaction.image_path = file_path

        # Commit the transaction to save all changes
        db.commit()
        logging.info("Database commit successful.")

        # Refresh the receipt instance to get the latest data
        db.refresh(receipt)

        return {"status": "success", "text": text, "image_path": file_path}
    except Exception as e:
        logging.error(f"Error during receipt upload: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
