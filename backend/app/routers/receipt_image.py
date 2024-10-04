# receipt_image.py is a FastAPI router that handles requests related to receipt images.
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, oauth2


router = APIRouter()

@router.get("/receipt_image/{transaction_id}")
async def get_receipt_image(transaction_id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # Fetch the transaction to find the image path
    transaction = db.query(models.CreditCardTransaction).filter(models.CreditCardTransaction.id == transaction_id).first()
    if transaction and transaction.image_path:
        return FileResponse(path=transaction.image_path, media_type='image/jpeg')
    else:
        raise HTTPException(status_code=404, detail="Receipt image not found")
