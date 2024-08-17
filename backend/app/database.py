from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# Fetching environment variables with fallback options
DATABASE_HOSTNAME = os.getenv("DATABASE_HOSTNAME", "localhost")
DATABASE_PORT = os.getenv("DATABASE_PORT", "5432")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD", "")
DATABASE_NAME = os.getenv("DATABASE_NAME", "")
DATABASE_USERNAME = os.getenv("DATABASE_USERNAME", "postgres")

# Construct the database URL
DATABASE_URL = f"postgresql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOSTNAME}:{DATABASE_PORT}/{DATABASE_NAME}"

# Setting up SQLAlchemy
engine = create_engine(DATABASE_URL, echo=True)  # echo=True for logging SQL statements (optional)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


