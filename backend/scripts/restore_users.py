import pandas as pd
from sqlalchemy import create_engine, Table, MetaData, text
from sqlalchemy.orm import sessionmaker
import bcrypt

# Database connection
engine = create_engine('postgresql://postgres:Guitar0123!@localhost:5432/crewone2')
Session = sessionmaker(bind=engine)
session = Session()

# Load CSV into a DataFrame
csv_path = r'C:\Users\dahern\Documents\ScheduleProjectUploads\TO UPLOAD 090324\users.csv'
df = pd.read_csv(csv_path)

# Print the column names to verify
print("Columns in CSV:", df.columns)

# Check if the 'Password' column exists
if 'Password' in df.columns:
    # Convert all passwords to strings and hash them before insertion
    df['hashed_password'] = df['Password'].apply(lambda x: bcrypt.hashpw(str(x).encode('utf-8'), bcrypt.gensalt()).decode('utf-8'))
    df.drop(columns=['Password'], inplace=True)  # Remove the original 'Password' column
else:
    print("Error: 'Password' column not found in the CSV file.")
    # Exit the script if the column is missing
    session.close()
    exit(1)

# Clear existing records in the users table
with engine.connect() as connection:
    connection.execute(text("TRUNCATE TABLE users RESTART IDENTITY CASCADE;"))

# Insert data into the users table
df.to_sql('users', engine, if_exists='append', index=False)

# Close the session
session.close()



