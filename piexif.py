import os
import shutil
from datetime import datetime
import subprocess

def get_creation_date(file_path):
    try:
        if file_path.lower().endswith(('.jpg', '.jpeg', '.png')):
            return get_image_creation_date(file_path)
        elif file_path.lower().endswith(('.mp4', '.mov')):
            return get_video_creation_date(file_path)
    except Exception as e:
        print(f"Error getting creation date for {file_path}: {e}")
    return None

def get_image_creation_date(image_path):
    try:
        from PIL import Image
        from PIL.ExifTags import TAGS
        
        image = Image.open(image_path)
        exif_data = image._getexif()
        if exif_data:
            for tag, value in exif_data.items():
                tag_name = TAGS.get(tag, tag)
                if tag_name == 'DateTimeOriginal':
                    return datetime.strptime(value, '%Y:%m:%d %H:%M:%S')
    except Exception as e:
        print(f"Error getting creation date for {image_path}: {e}")
    return None

def get_video_creation_date(video_path):
    try:
        result = subprocess.run(['exiftool', '-CreationDate', '-d', '%Y:%m:%d %H:%M:%S', '-s', '-S', video_path], capture_output=True, text=True)
        if result.returncode == 0:
            creation_date_str = result.stdout.strip()
            if creation_date_str:
                return datetime.strptime(creation_date_str, '%Y:%m:%d %H:%M:%S')
    except Exception as e:
        print(f"Error getting creation date for {video_path}: {e}")
    return None

def export_files_with_original_dates(source_folder, dest_folder):
    try:
        for root, dirs, files in os.walk(source_folder):
            for file_name in files:
                source_path = os.path.join(root, file_name)
                creation_date = get_creation_date(source_path)
                if creation_date:
                    dest_path = os.path.join(dest_folder, file_name)
                    shutil.copy2(source_path, dest_path)
                    os.utime(dest_path, (creation_date.timestamp(), creation_date.timestamp()))
                    print(f"Exported {file_name} with original creation date.")
                else:
                    print(f"Could not retrieve creation date for {source_path}. Skipping export.")
    except Exception as e:
        print(f"Error exporting files: {e}")

# Example usage
source_folder = "/Users/szilardmate/desktop/src"
destination_folder = "/Users/szilardmate/desktop/destination/"
export_files_with_original_dates(source_folder, destination_folder)