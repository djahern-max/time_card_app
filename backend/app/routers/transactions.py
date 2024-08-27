from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
import io
import csv

from app.database import get_db
from app import models

router = APIRouter()

@router.get("/export_transactions")
def export_transactions(db: Session = Depends(get_db)):
    # Query the database
    transactions = db.query(models.CreditCardTransaction).all()

    # Create a CSV file in memory
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["id", "emp_code", "card_last_four", "statement_date", "transaction_date", "amount", "description", "coding", "employee_coding", "image_path"])

    for transaction in transactions:
        writer.writerow([
            transaction.id,
            transaction.emp_code,
            transaction.card_last_four,
            transaction.statement_date,
            transaction.transaction_date,
            transaction.amount,
            transaction.description,
            transaction.coding,
            transaction.employee_coding,
            transaction.image_path
        ])

    output.seek(0)
    return StreamingResponse(output, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=credit_card_transactions.csv"})
