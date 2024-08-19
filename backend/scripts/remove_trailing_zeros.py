import pandas as pd

def remove_trailing_zeros(file_path):
    # Load the CSV file into a DataFrame
    df = pd.read_csv(file_path)

    # Apply the function to remove trailing zeros from all string columns
    df = df.applymap(lambda x: str(x).rstrip('0').rstrip('.') if isinstance(x, str) and '.' in x else x)

    # Save the cleaned data back to a new CSV file
    output_file = file_path.replace('.csv', '_cleaned.csv')
    df.to_csv(output_file, index=False)
    print(f"Trailing zeros removed. Cleaned file saved as {output_file}")

if __name__ == "__main__":
    # Specify the path to your CSV file
    csv_file_path = r"C:\Users\dahern\Documents\ScheduleProjectUploads\TimeCards.csv"
    
    remove_trailing_zeros(csv_file_path)

