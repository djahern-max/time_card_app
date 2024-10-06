#models.py will contain the SQLAlchemy models for the database tables. We will define the following models:
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Boolean, Enum as SQLAEnum, Numeric, Text, DateTime, func
from sqlalchemy.orm import relationship
from .database import Base
import enum


class UserRole(enum.Enum):
    mechanic = "mechanic"
    general = "general"
    admin = "admin"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    role = Column(SQLAEnum(UserRole), default=UserRole.general)  # Using enum for roles
    emp_code = Column(String)

    mechanics_time_reports = relationship("MechanicsTimeReport", back_populates="user")
    daily_time_reports = relationship("DailyTimeReport", back_populates="user")
    receipts = relationship("Receipt", back_populates="user")
    bulk_uploads = relationship("BulkReceiptUpload", back_populates="admin_user")

class MechanicsTimeReport(Base):
    __tablename__ = "mechanics_time_reports"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    date = Column(Date)
    hours_worked = Column(Integer)
    equipment = Column(String)
    equipment_number = Column(String)
    cost_category = Column(String)
    work_order_number = Column(String)
    description = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="mechanics_time_reports")

class DailyTimeReport(Base):
    __tablename__ = "daily_time_reports"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    date = Column(Date)
    hours_worked = Column(Integer)
    job_name = Column(String)
    description = Column(String)
    equipment = Column(String)
    loads = Column(String)
    pit = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="daily_time_reports")

class JobPhase(Base):
    __tablename__ = "job_phases"

    id = Column(Integer, primary_key=True, index=True)
    job = Column(String, index=True, nullable=False)
    phase_number = Column(String, index=True, nullable=False)
    phase_name = Column(String, nullable=True)
    cost_type = Column(String, nullable=True)

# Equipment Model
class Equipment(Base):
    __tablename__ = "equipment"

    id = Column(Integer, primary_key=True, index=True)
    equipment_number = Column(String, nullable=False)
    equipment_name = Column(String, nullable=False)
    equipment_type = Column(String, nullable=False)



class Employee(Base):
    __tablename__ = "employees"

    emp_code = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    street_address = Column(String, nullable=False)
    town = Column(String, nullable=False)
    zip = Column(String, nullable=False)
    hire_date = Column(Date, nullable=False)
    marital_status = Column(String, nullable=False)
    comp_code = Column(String, nullable=False)
    general_department = Column(String, nullable=False)
    department = Column(String, nullable=False)
    department_code = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    hourly_salary = Column(String, nullable=False)
    pay_type_code = Column(String, nullable=False)
    date_of_birth = Column(Date, nullable=False)
    title = Column(String, nullable=False)
    pay_rate = Column(String, nullable=False)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)

# Timecard Model
class Timecard(Base):
    __tablename__ = "timecards"

    id = Column(Integer, primary_key=True, index=True)
    emp_code = Column(String, nullable=False)
    name = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    hours_worked = Column(Integer, nullable=False)
    rate = Column(String, nullable=False)
    extension = Column(String, nullable=True)
    department = Column(String, nullable=False)
    job = Column(String, nullable=False)
    phase = Column(String, nullable=False)

# models.py

class CreditCardTransaction(Base):
    __tablename__ = "credit_card_transactions"

    id = Column(Integer, primary_key=True, index=True)
    emp_code = Column(String, nullable=False)
    card_last_four = Column(String, nullable=False)
    statement_date = Column(Date, nullable=False)
    transaction_date = Column(Date, nullable=False)
    amount = Column(Numeric, nullable=False)
    description = Column(String, nullable=True)
    coding = Column(String, nullable=True)
    employee_coding = Column(String, nullable=True)
    image_path = Column(String, nullable=True)
    bulk_upload_id = Column(Integer, ForeignKey("bulk_receipt_uploads.id"))

    # Define the relationship to the Receipt model
    receipts = relationship("Receipt", back_populates="transaction")

    bulk_upload = relationship("BulkReceiptUpload", back_populates="transactions")




class Receipt(Base):
    __tablename__ = "receipts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    transaction_id = Column(Integer, ForeignKey("credit_card_transactions.id"))
    emp_code = Column(String(10), nullable=False)
    filename = Column(String, index=True)
    upload_date = Column(DateTime(timezone=True), server_default=func.now())
    text = Column(String)
    coding = Column(String)
    employee_coding = Column(String)
    image_path = Column(String)

    transaction = relationship("CreditCardTransaction", back_populates="receipts")
    user = relationship("User", back_populates="receipts")


class BulkReceiptUpload(Base):
    __tablename__ = "bulk_receipt_uploads"

    id = Column(Integer, primary_key=True, index=True)
    admin_user_id = Column(Integer, ForeignKey("users.id"))
    upload_date = Column(DateTime(timezone=True), server_default=func.now())
    file_name = Column(String)
    status = Column(String)  # e.g., 'processing', 'completed', 'failed'
    total_receipts = Column(Integer)
    matched_receipts = Column(Integer)
    unmatched_receipts = Column(Integer)

    # Add this relationship if it's supposed to link to transactions
    transactions = relationship("CreditCardTransaction", back_populates="bulk_upload")

    admin_user = relationship("User", back_populates="bulk_uploads")



