from fastapi import APIRouter
import subprocess
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize router (not app)
router = APIRouter()

@router.post("/download-statements")
def download_statements():
    try:
        # Run the Selenium script using subprocess
        subprocess.run(["python", "backend/scripts/statement_downloader.py"], check=True)
        return {"message": "Statements downloaded successfully!"}
    except subprocess.CalledProcessError as e:
        return {"error": f"An error occurred: {e}"}
