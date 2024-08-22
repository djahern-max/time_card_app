import os
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import pytesseract
from PIL import Image

router = APIRouter()

# Specify the directory where uploaded files will be stored
UPLOAD_DIRECTORY = r"C:\Users\dahern\Documents\ScheduleProjectUploads\Receipt Images"

# Ensure the directory exists
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

@router.post("/upload_receipt")
async def upload_receipt(file: UploadFile = File(...)):
    try:
        # Save the file to the specified directory
        file_path = os.path.join(UPLOAD_DIRECTORY, file.filename)
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())

        # Use pytesseract to extract text from the image
        image = Image.open(file_path)
        text = pytesseract.image_to_string(image)

        return JSONResponse(content={"status": "success", "text": text})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



