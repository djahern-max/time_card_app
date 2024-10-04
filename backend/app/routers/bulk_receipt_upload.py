# bulk_receipt_upload.py
from fastapi import APIRouter, File, UploadFile, Depends, HTTPException
from sqlalchemy.orm import Session
from pdf2image import convert_from_bytes
import io
import pytesseract
from PIL import Image
from . import models, oauth2
from app.database import get_db
from sqlalchemy.exc import SQLAlchemyError
import re
from datetime import datetime

router = APIRouter()

def extract_amount(text):
    # Simple regex to find a dollar amount
    match = re.search(r'\$?\d+\.\d{2}', text)
    return float(match.group().replace('$', '')) if match else None

def extract_date(text):
    # Simple regex to find a date (assumes MM/DD/YYYY format)
    match = re.search(r'\d{2}/\d{2}/\d{4}', text)
    return datetime.strptime(match.group(), '%m/%d/%Y').date() if match else None

def extract_description(text):
    # This is a placeholder. You'll need to implement this based on your receipt format
    return text[:100]  # Just return the first 100 characters as a description

def process_image(image):
    # Extract text using OCR
    text = pytesseract.image_to_string(image)
    # Parse the text to extract relevant information
    amount = extract_amount(text)
    date = extract_date(text)
    description = extract_description(text)
    return {"amount": amount, "date": date, "description": description}

def find_matching_transaction(db: Session, receipt_data):
    return db.query(models.CreditCardTransaction).filter(
        models.CreditCardTransaction.amount == receipt_data['amount'],
        models.CreditCardTransaction.transaction_date == receipt_data['date']
    ).first()

def update_transaction_with_receipt(db: Session, transaction, receipt_data, image):
    # Save image to file system and get path
    image_path = save_image(image)
    
    # Update transaction
    transaction.description = receipt_data['description']
    transaction.image_path = image_path
    db.commit()

def save_image(image):
    # Implement this function to save the image to your file system
    # and return the path where it was saved
    pass

@router.post("/admin/bulk_upload_receipts")
async def bulk_upload_receipts(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized")

    try:
        pdf_content = await file.read()
        images = convert_from_bytes(pdf_content)
        
        results = []
        for image in images:
            receipt_data = process_image(image)
            
            # Find matching transaction
            transaction = find_matching_transaction(db, receipt_data)
            
            if transaction:
                # Update transaction with receipt info
                update_transaction_with_receipt(db, transaction, receipt_data, image)
                results.append({"status": "success", "transaction_id": transaction.id})
            else:
                results.append({"status": "no_match", "receipt_data": receipt_data})
        
        return {"results": results}
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")