import os
import pandas as pd
import numpy as np

def format_value(value):
    try:
        # Try to convert to float and format to 2 decimal places
        return f"{float(value):.2f}"
    except ValueError:
        # If conversion fails, return the original value
        return value

def combine_csv_files(input_folder, output_file):
    # List all CSV files in the input folder
    csv_files = [f for f in os.listdir(input_folder) if f.endswith('.csv')]

    # Check if there are CSV files to combine
    if not csv_files:
        print("No CSV files found in the directory.")
        return

    combined_data = pd.DataFrame()

    # Iterate through each CSV file
    for file in csv_files:
        file_path = os.path.join(input_folder, file)
        print(f"Processing file: {file_path}")
        
        try:
            # Read each CSV file, explicitly specifying column names
            df = pd.read_csv(file_path, header=0, names=['D', 'E', 'F', 'G', 'H', 'I', 'J'])
            
            # Ensure the dataframe has exactly 7 columns
            if len(df.columns) != 7:
                print(f"Skipping {file}: Incorrect number of columns")
                continue
            
            # Combine columns H and I, removing NaN and empty values, formatting numbers
            df['H'] = df.apply(lambda row: ' '.join(filter(lambda x: x != '' and x.lower() != 'nan', 
                                                           [format_value(x) for x in [row['H'], row['I']] if pd.notna(x)])), axis=1)
            df = df.drop(columns=['I'])
            
            # Add blank column 'A' at the beginning
            df.insert(0, 'A', '')
            
            # Add another blank column 'B'
            df.insert(1, 'B', '')
            
            # Add '08/26/2024' as column 'C'
            df.insert(2, 'C', '08/26/2024')
            
            combined_data = pd.concat([combined_data, df], ignore_index=True)
        except Exception as e:
            print(f"Error processing file {file}: {e}")
            continue

    # Save the combined data into a new CSV file
    combined_data.to_csv(output_file, index=False)
    print(f"Combined file saved to {output_file}")

if __name__ == "__main__":
    # Define the folder containing the downloaded CSV files
    input_folder = r"C:\Users\dahern\Documents\timecard-app\backend\downloadedStatements"
    
    # Define the output file path (saved in the same folder)
    output_file = os.path.join(input_folder, "combined_statements.csv")

    # Combine the CSV files
    combine_csv_files(input_folder, output_file)