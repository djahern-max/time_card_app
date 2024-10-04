# credit_card_transactions.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, models
from app.database import get_db
from typing import List
from sqlalchemy import text

router = APIRouter()

@router.get("/credit_card_transactions", response_model=List[schemas.CreditCardTransactionSchema])
def get_credit_card_transactions(db: Session = Depends(get_db)):
    try:
        transactions = db.execute(
            text(
                """
                SELECT
                    c.id,
                    c.transaction_date AS date,
                    c.emp_code,
                    c.card_last_four,
                    c.amount,
                    c.description,
                    c.coding,
                    c.employee_coding,
                    c.image_path,
                    c.bulk_upload_id
                FROM
                    credit_card_transactions c
                ORDER BY
                    c.transaction_date ASC;
                """
            )
        ).fetchall()

        transactions_list = [
            {
                "id": row.id,
                "date": row.date.strftime("%Y-%m-%d"),
                "emp_code": row.emp_code,
                "card_last_four": row.card_last_four,
                "amount": float(row.amount),  # Convert Decimal to float
                "description": row.description,
                "coding": row.coding,
                "employee_coding": row.employee_coding or None,
                "image_path": row.image_path or None,
                "bulk_upload_id": row.bulk_upload_id  # Add this line
            }
            for row in transactions
        ]

        return transactions_list
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
