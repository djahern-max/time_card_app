from fastapi import FastAPI
from .routers import auth, timecards, upload, schedule, credit_card_transactions, receipt_image, transactions, ocr, bulk_receipt_upload, download_statements
from .database import engine, Base
from . import models
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

# Initialize logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application startup")

    # List all routes in the app after startup
    for route in app.routes:
        logger.info(f"Path: {route.path}, Methods: {route.methods}")

    Base.metadata.create_all(bind=engine)
    yield
    logger.info("Application shutdown")

# Create the FastAPI app instance with the lifespan context
app = FastAPI(lifespan=lifespan)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins for testing (can be restricted in production)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, PUT, DELETE)
    allow_headers=["*"],  # Allows all headers
)

# Include routers
app.include_router(auth.router)
app.include_router(timecards.router)
app.include_router(upload.router)
app.include_router(schedule.router)
app.include_router(ocr.router)
app.include_router(credit_card_transactions.router)
app.include_router(receipt_image.router)
app.include_router(transactions.router)
app.include_router(bulk_receipt_upload.router)  # Include bulk receipt upload router
app.include_router(download_statements.router)  # Include the new download_statements router
