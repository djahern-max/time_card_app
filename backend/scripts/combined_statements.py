import os
import pandas as pd
import re

def format_value(value):
    try:
        float_value = float(value)
        if float_value.is_integer():
            return f"{float_value:.2f}"
        else:
            return str(float_value)
    except ValueError:
        return value

def extract_info_from_filename(filename):
    match = re.match(r'StmtClosing(\d{8})_(.+?)(\d{4})\.csv$', filename)
    if match:
        statement_date = match.group(1)
        emp_code = match.group(2).strip()
        card_last_four = match.group(3)
        return emp_code, card_last_four, statement_date
    return '', '', ''

def combine_csv_files(input_folder, output_file):
    csv_files = [f for f in os.listdir(input_folder) if f.endswith('.csv')]

    if not csv_files:
        print("No CSV files found in the directory.")
        return

    combined_data = pd.DataFrame(columns=[
        'emp_code', 'card_last_four', 'statement_date', 'transaction_date', 
        'amount', 'description', 'coding', 'employee_coding', 'image_path'
    ])

    for file in csv_files:
        file_path = os.path.join(input_folder, file)
        print(f"Processing file: {file_path}")
        
        try:
            df = pd.read_csv(file_path, header=None)

            emp_code, card_last_four, statement_date = extract_info_from_filename(file)

            # Column indices may need adjusting depending on the exact structure of your CSVs
            df['transaction_date'] = df.iloc[:, 1]  # Column B for transaction date
            df['description'] = df.iloc[:, 4]       # Column E for description
            
            # Combine F and G into a single 'amount' column
            df['amount'] = df.apply(lambda row: -float(format_value(row[5])) if pd.notna(row[5]) and row[5] != '' 
                                    else float(format_value(row[6])), axis=1)

            # Create the final dataframe with selected columns
            df = df[['transaction_date', 'amount', 'description']]
            df['emp_code'] = emp_code
            df['card_last_four'] = card_last_four
            df['statement_date'] = statement_date
            df['coding'] = ''
            df['employee_coding'] = ''
            df['image_path'] = ''
            
            # Reorder the columns to match the desired output
            df = df[['emp_code', 'card_last_four', 'statement_date', 'transaction_date', 'amount', 
                     'description', 'coding', 'employee_coding', 'image_path']]
            
            combined_data = pd.concat([combined_data, df], ignore_index=True)

        except Exception as e:
            print(f"Error processing file {file}: {e}")
            continue

    combined_data.to_csv(output_file, index=False)
    print(f"Combined file saved to {output_file}")

if __name__ == "__main__":
    # Correct input folder path
    input_folder = r"C:\Users\dahern\Documents\timecard-app\backend\downloadedStatements"
    output_file = os.path.join(input_folder, "combined_statements.csv")
    combine_csv_files(input_folder, output_file)


