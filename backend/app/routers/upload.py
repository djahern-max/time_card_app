from fastapi import APIRouter, File, UploadFile
import pandas as pd
from sqlalchemy import create_engine
from io import StringIO
import logging

router = APIRouter()

@router.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        logging.info("File read successfully")
        
        # Use StringIO to read the contents of the CSV file
        df = pd.read_csv(StringIO(contents.decode('utf-8')))
        logging.info("CSV file parsed into DataFrame")

        # Database connection
        engine = create_engine('postgresql://postgres:Guitar0123!@localhost:5432/crewone2')
        logging.info("Database connection established")

        # Upload the data to the employees table
        df.to_sql('employees', engine, if_exists='append', index=False)
        logging.info("Data uploaded to database")

        return {"filename": file.filename, "status": "success"}
    except Exception as e:
        logging.error(f"Error occurred: {e}")
        return {"error": str(e)}


