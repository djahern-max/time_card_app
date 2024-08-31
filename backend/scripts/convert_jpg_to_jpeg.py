import os
from PIL import Image

# Paths
input_dir = r'C:\Users\dahern\Documents\ScheduleProjectUploads\Receipt_Images\jpg'
output_dir = r'C:\Users\dahern\Documents\ScheduleProjectUploads\Receipt_Images\jpeg'

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# List of supported file extensions
supported_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.heic']  # Add other formats as needed

# Convert images to JPEG
for filename in os.listdir(input_dir):
    ext = os.path.splitext(filename)[1].lower()
    if ext in supported_extensions:
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, os.path.splitext(filename)[0] + '.jpeg')
        
        try:
            # Open image using Pillow
            with Image.open(input_path) as img:
                # Convert and save as JPEG
                img = img.convert('RGB')  # Ensure compatibility with JPEG format
                img.save(output_path, 'JPEG')
            print(f"Converted {filename} to JPEG.")
        except Exception as e:
            print(f"Error processing {filename}: {e}")

print('Conversion complete.')

