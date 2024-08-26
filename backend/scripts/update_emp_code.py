import sys
import os
from sqlalchemy.orm import Session

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')

from app.database import SessionLocal
from app.models import User, Employee

def update_emp_code_from_employees():
    db: Session = SessionLocal()
    
    # Fetch all users
    users = db.query(User).all()
    
    for user in users:
        # Find the corresponding employee with the same username
        employee = db.query(Employee).filter(Employee.username == user.username).first()
        
        if employee:
            # Update the emp_code in the users table
            user.emp_code = employee.emp_code
            print(f"Updated emp_code for {user.username} to {employee.emp_code}")
        else:
            print(f"No matching employee found for {user.username}")

    # Commit all changes to the database
    db.commit()
    db.close()

if __name__ == "__main__":
    update_emp_code_from_employees()
    print("emp_code column updated successfully based on employees table.")


