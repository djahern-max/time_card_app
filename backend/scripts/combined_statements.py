import os
import pandas as pd
import numpy as np
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
    print(f"Extracting info from filename: {filename}")  # Debug print
    # Extract information from filename
    match = re.match(r'StmtClosing(\d{8})_(.+?)(\d{4})\.csv$', filename)
    if match:
        date = match.group(1)
        employee_name = match.group(2).strip()
        card_last_four = match.group(3)
        # Remove any trailing underscore from the employee name
        employee_name = employee_name.rstrip('_')
        print(f"Extracted: Date={date}, Name={employee_name}, Card={card_last_four}")  # Debug print
        return employee_name, card_last_four
    print(f"No match found for filename: {filename}")  # Debug print
    return '', ''  # Return empty strings if the pattern doesn't match

def combine_csv_files(input_folder, output_file):
    csv_files = [f for f in os.listdir(input_folder) if f.endswith('.csv')]

    if not csv_files:
        print("No CSV files found in the directory.")
        return

    combined_data = pd.DataFrame()

    for file in csv_files:
        file_path = os.path.join(input_folder, file)
        print(f"Processing file: {file_path}")
        
        try:
            df = pd.read_csv(file_path, header=0, names=['D', 'E', 'F', 'G', 'H', 'I', 'J'])
            
            if len(df.columns) != 7:
                print(f"Skipping {file}: Incorrect number of columns")
                continue
            
            # Extract employee name and card_last_four from filename
            employee_name, card_last_four = extract_info_from_filename(file)
            
            print(f"Extracted name: {employee_name}, card: {card_last_four}")  # Debug print
            
            # Combine columns H and I, removing NaN and empty values, formatting numbers
            df['H'] = df.apply(lambda row: ' '.join(filter(lambda x: x != '' and x.lower() != 'nan', 
                                                           [format_value(x) for x in [row['H'], row['I']] if pd.notna(x)])), axis=1)
            df = df.drop(columns=['I'])
            
            # Add employee name as column 'A'
            df.insert(0, 'A', employee_name)
            
            # Add card_last_four as column 'B'
            df.insert(1, 'B', card_last_four)
            
            # Add '08/26/2024' as column 'C'
            df.insert(2, 'C', '08/26/2024')
            
            combined_data = pd.concat([combined_data, df], ignore_index=True)
        except Exception as e:
            print(f"Error processing file {file}: {e}")
            continue

    combined_data.to_csv(output_file, index=False)
    print(f"Combined file saved to {output_file}")
    print(f"First few rows of combined data:\n{combined_data.head()}")  # Debug print

if __name__ == "__main__":
    input_folder = r"C:\Users\dahern\Documents\timecard-app\backend\downloadedStatements"
    output_file = os.path.join(input_folder, "combined_statements.csv")
    combine_csv_files(input_folder, output_file)