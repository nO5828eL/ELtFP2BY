# 代码生成时间: 2025-09-03 23:45:42
import os
from celery import Celery

# Celery configuration
app = Celery('folder_structure_manager')
app.config_from_object('celeryconfig')

# Define the task to organize the folder structure
@app.task
def organize_folder_structure(source_folder, destination_folder, file_map):
    '''
    Organize the folder structure by moving files according to the file_map dictionary.

    :param source_folder: The path of the source folder to organize files from.
    :param destination_folder: The path of the destination folder to organize files to.
    :param file_map: A dictionary with file extensions as keys and destination subfolders as values.
    '''
    # Check if source folder exists
    if not os.path.exists(source_folder):
        raise FileNotFoundError(f"Source folder '{source_folder}' does not exist.")

    # Check if destination folder exists, create if not
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # Iterate over file_map and move files accordingly
    for file_extension, subfolder in file_map.items():
        subfolder_path = os.path.join(destination_folder, subfolder)
        if not os.path.exists(subfolder_path):
            os.makedirs(subfolder_path)
        for root, dirs, files in os.walk(source_folder):
            for file in files:
                if file.endswith(file_extension):
                    src_file_path = os.path.join(root, file)
                    dst_file_path = os.path.join(subfolder_path, file)
                    try:
                        os.rename(src_file_path, dst_file_path)
                    except OSError as e:
                        # Handle file move errors
                        print(f"Error moving file {src_file_path} to {dst_file_path}: {e}")

# Example usage of the task
if __name__ == '__main__':
    # Define the file map
    file_map = {
        '.jpg': 'images',
        '.txt': 'documents',
        '.pdf': 'pdfs'
    }

    # Define the source and destination folders
    source_folder = '/path/to/source'
    destination_folder = '/path/to/destination'

    # Call the task
    organize_folder_structure.delay(source_folder, destination_folder, file_map)