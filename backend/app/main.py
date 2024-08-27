from fastapi import FastAPI
from .routers import auth, timecards, upload, schedule, credit_card_transactions, receipt_image, transactions
from .database import engine
from . import models
from fastapi.middleware.cors import CORSMiddleware
from .routers import ocr

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allows specific origin
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allows all headers
)

app.include_router(auth.router)
app.include_router(timecards.router)
app.include_router(upload.router)
app.include_router(timecards.router)
app.include_router(schedule.router)
app.include_router(ocr.router)
app.include_router(credit_card_transactions.router)
app.include_router(receipt_image.router)
app.include_router(transactions.router)