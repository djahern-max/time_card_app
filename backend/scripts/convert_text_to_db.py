import os
from datetime import datetime
import psycopg2

def parse_and_insert_transactions(txt_file_path, emp_code, card_last_four, statement_date):
    # Connect to the PostgreSQL database
    conn = psycopg2.connect(
        dbname="crewone2",
        user="postgres",
        password="Guitar0123!",
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()

    with open(txt_file_path, 'r') as file:
        for line in file:
            parts = line.split(',')

            # Extracting data and stripping any extra whitespace or quotation marks
            transaction_date_str = parts[0].strip()
            amount_str = parts[1].strip() or parts[2].strip()  # Handles both debit and credit amounts
            description = parts[4].strip().strip('"')

            # Parse the transaction date and amount
            transaction_date = datetime.strptime(transaction_date_str, '%m/%d/%Y').date()
            amount = float(amount_str)

            # Insert the transaction into the database
            cursor.execute("""
                INSERT INTO credit_card_transactions (emp_code, card_last_four, statement_date, transaction_date, amount, description)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (emp_code, card_last_four, statement_date, transaction_date, amount, description))

    conn.commit()
    cursor.close()
    conn.close()

def process_multiple_files(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            filename_parts = filename.replace('.txt', '').split()
            emp_code = filename_parts[0]
            card_last4 = filename_parts[1]
            statement_date = datetime.strptime(filename_parts[2], '%m%d%y').date()

            txt_file_path = os.path.join(directory, filename)
            parse_and_insert_transactions(txt_file_path, emp_code, card_last4, statement_date)

# Example usage
process_multiple_files(r'C:\Users\dahern\Documents\ScheduleProjectUploads\CC Uploads')


