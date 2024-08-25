import os
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Form
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app import models, database, oauth2
import pytesseract
from PIL import Image

router = APIRouter()

# Specify the directory where uploaded files will be stored
UPLOAD_DIRECTORY = r"C:\Users\dahern\Documents\ScheduleProjectUploads\Receipt Images"

# Ensure the directory exists
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

@router.post("/upload_receipt")
async def upload_receipt(
    file: UploadFile = File(...),
    coding: str = Form(...),  # Accept coding information from the frontend
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
            coding=coding,  # Store the coding information
            emp_code=emp_code,
            transaction_id=transaction_id  # Store the transaction_id to link with the transaction
        )
        db.add(receipt)
        db.commit()
        db.refresh(receipt)

        return JSONResponse(content={"status": "success", "text": text, "image_path": file_path})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


