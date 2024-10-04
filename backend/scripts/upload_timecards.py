import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Database connection
engine = create_engine('postgresql://postgres:Guitar0123!@localhost:5432/crewone2')
Session = sessionmaker(bind=engine)
session = Session()

# Load CSV into a DataFrame
csv_path = r'C:\Users\dahern\Documents\ScheduleProjectUploads\TO UPLOAD 090324\TimeCards.csv'
df = pd.read_csv(csv_path)

# Print the column names to verify
print("Columns in CSV:", df.columns)

# Ensure the DataFrame matches the table structure
required_columns = ['emp_code', 'name', 'date', 'hours_worked', 'rate', 'extension', 'department', 'job', 'phase']
missing_columns = [col for col in required_columns if col not in df.columns]
if missing_columns:
    print(f"Error: Missing columns in CSV: {missing_columns}")
    session.close()
    exit(1)

# Insert data into the timecards table
df.to_sql('timecards', engine, if_exists='append', index=False)

# Close the session
session.close()

print("Data successfully uploaded to the timecards table.")

