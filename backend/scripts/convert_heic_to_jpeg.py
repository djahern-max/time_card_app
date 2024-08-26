import os
from PIL import Image
import pillow_heif

# Paths
input_dir = r'C:\Users\dahern\Documents\ScheduleProjectUploads\Receipt_Images\HEIC'
output_dir = r'C:\Users\dahern\Documents\ScheduleProjectUploads\Receipt_Images\jpeg'

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Register the HEIC format with Pillow
pillow_heif.register_heif_opener()

# Convert HEIC to JPEG
for filename in os.listdir(input_dir):
    if filename.lower().endswith('.heic'):
        heic_path = os.path.join(input_dir, filename)
        jpeg_path = os.path.join(output_dir, os.path.splitext(filename)[0] + '.jpeg')

        # Open HEIC file using Pillow
        with Image.open(heic_path) as img:
            # Save as JPEG
            img.save(jpeg_path, 'JPEG')

print('Conversion complete.')


