import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Database connection
engine = create_engine('postgresql://postgres:Guitar0123!@localhost:5432/crewone2')
Session = sessionmaker(bind=engine)
session = Session()

# Load CSV into a DataFrame
csv_path = r'C:\Users\dahern\Documents\ScheduleProjectUploads\TO UPLOAD 082624\StmtClosing20240826_BEMIS1398.csv'
df = pd.read_csv(csv_path)

# Clean column names to remove any leading/trailing spaces
df.columns = df.columns.str.strip()

# Drop the 'id' column to allow the database to auto-generate IDs
if 'id' in df.columns:
    df = df.drop(columns=['id'])

# Ensure all date columns are in the correct format
df['statement_date'] = pd.to_datetime(df['statement_date'], format='%m/%d/%Y')
df['transaction_date'] = pd.to_datetime(df['transaction_date'], format='%m/%d/%Y')

# Handle both negative values in parentheses and with minus sign
# 1. Replace parentheses with minus sign for values like "(492.97)"
# 2. Convert the entire 'amount' column to numeric values
df['amount'] = df['amount'].replace(r'\((.*?)\)', r'-\1', regex=True)  # Convert parentheses to negative numbers
df['amount'] = pd.to_numeric(df['amount'], errors='coerce')  # Ensure numeric format, 'coerce' converts invalid values to NaN

# Insert data into the credit_card_transactions table
df.to_sql('credit_card_transactions', engine, if_exists='append', index=False)

# Close the session
session.close()

print("Data successfully uploaded to the credit_card_transactions table.")







