import pandas as pd
import bcrypt
from sqlalchemy import create_engine

# Load the CSV file
file_path = 'C:/Users/dahern/Documents/ScheduleProjectUploads/EmployeeListing.csv'
employee_data = pd.read_csv(file_path)

# Ensure that the password column is treated as strings
employee_data['password'] = employee_data['password'].astype(str)

# Hash the passwords using bcrypt
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# Apply the hashing function to the password column
employee_data['hashed_password'] = employee_data['password'].apply(hash_password)

# Prepare the data to be inserted into the users table
users_data = employee_data[['username', 'hashed_password', 'role']]
users_data['is_active'] = True  # Assuming all users are active

# Connect to the PostgreSQL database
engine = create_engine('postgresql://postgres:Guitar0123!@localhost:5432/crewone2')

# Insert the data into the users table
users_data.to_sql('users', engine, if_exists='append', index=False)

print("Users have been successfully created and inserted into the database.")


