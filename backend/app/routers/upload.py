from fastapi import APIRouter, File, UploadFile, HTTPException, Query, Depends
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from io import StringIO
import pandas as pd
import logging
from app import models
from app.database import get_db
import csv
from io import StringIO


router = APIRouter()

# General upload route for different datasets
@router.post("/upload/")
async def upload_file(file: UploadFile = File(...), dataset: str = Query(..., description="Specify the dataset type")):
    try:
        contents = await file.read()
        df = pd.read_csv(StringIO(contents.decode('utf-8')))
        logging.info(f"CSV file parsed into DataFrame for dataset: {dataset}")

        # Database connection
        engine = create_engine('postgresql://postgres:Guitar0123!@localhost:5432/crewone2')
        logging.info("Database connection established")

        # Process based on dataset type
        if dataset == 'employees':
            table_name = 'employees'
        elif dataset == 'jobs':
            table_name = 'jobs'
        elif dataset == 'equipment':
            table_name = 'equipment'
        else:
            raise HTTPException(status_code=400, detail="Invalid dataset type")

        # Upload the data to the corresponding table
        df.to_sql(table_name, engine, if_exists='append', index=False)
        logging.info(f"Data uploaded to {table_name} table in the database")

        return {"filename": file.filename, "status": "success", "dataset": dataset}

    except Exception as e:
        logging.error(f"Error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/upload/jobs/")
async def upload_jobs(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        # Read the contents of the file
        contents = await file.read()
        
        # Read the CSV file into a DataFrame
        df = pd.read_csv(StringIO(contents.decode('utf-8')))
        
        # Convert all columns to strings
        df = df.astype(str)

        # Strip any leading/trailing whitespace from each field
        df = df.applymap(str.strip)

        # Iterate through the DataFrame and insert each row into the database
        for _, row in df.iterrows():
            job_phase = models.JobPhase(
                job=row['job'],
                phase_number=row['phase_number'],
                phase_name=row['phase_name'],
                cost_type=row['cost_type']
            )
            db.add(job_phase)
        
        # Commit the transaction
        db.commit()

        return {"filename": file.filename, "status": "success"}

    except Exception as e:
        db.rollback()
        logging.error(f"Error occurred: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    
@router.post("/upload/equipment/")
async def upload_equipment(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        contents = await file.read()
        decoded_content = contents.decode('utf-8')
        csv_reader = csv.reader(StringIO(decoded_content))

        headers = next(csv_reader)  # Skip the header row if present
        for row in csv_reader:
            # Ensure every element is a string
            row = [str(cell) for cell in row]
            
            # Strip whitespace and assign values
            equipment_number = row[0].strip()
            equipment_name = row[1].strip()
            equipment_type = row[2].strip()

            # Create and add the equipment object to the database
            equipment = models.Equipment(
                equipment_number=equipment_number,
                equipment_name=equipment_name,
                equipment_type=equipment_type,
            )
            db.add(equipment)
        db.commit()

        return {"filename": file.filename, "status": "success"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))