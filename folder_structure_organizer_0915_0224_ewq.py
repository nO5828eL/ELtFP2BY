# 代码生成时间: 2025-09-15 02:24:58
import os
import shutil
from celery import Celery
from kombu import Queue

# Define the broker URL for Celery
broker_url = 'redis://localhost:6379/0'

# Create a Celery instance
app = Celery('folder_structure_organizer', broker=broker_url)

# Define the queues
app.conf.task_queues = (Queue('folder_structure_organizer_tasks', routing_key='folder_structure_organizer.#'),)

# Define the exchange
app.conf.task_exchange = 'folder_structure_organizer_exchange'
app.conf.task_exchange_type = 'direct'

# Function to organize the folder structure
@app.task()
def organize_folder_structure(source_folder, target_folder, extension):
    """
    Organize the folder structure by moving files with a specific extension
    from the source folder to the target folder.
    
    :param source_folder: The path to the source folder
    :param target_folder: The path to the target folder
    :param extension: The file extension to filter by
    """
    # Check if the source folder exists
    if not os.path.exists(source_folder):
        raise FileNotFoundError('Source folder does not exist')
    
    # Create the target folder if it does not exist
    os.makedirs(target_folder, exist_ok=True)
    
    # Iterate over the files in the source folder
    for filename in os.listdir(source_folder):
        # Check if the file has the specified extension
        if filename.endswith(extension):
            # Construct the full file path
            file_path = os.path.join(source_folder, filename)
            
            # Check if the file is actually a file and not a directory
            if os.path.isfile(file_path):
                # Move the file to the target folder
                shutil.move(file_path, target_folder)
                
                # Print a message to indicate the file was moved
                print(f'Moved {filename} to {target_folder}')
            else:
                # Print a message to indicate the file is a directory
                print(f'Skipping directory {filename}')
        else:
            # Print a message to indicate the file does not have the specified extension
            print(f'Skipping file {filename} as it does not have the {extension} extension')

# Example usage
if __name__ == '__main__':
    source = '/path/to/source/folder'
    target = '/path/to/target/folder'
    ext = '.txt'
    
    # Call the task to organize the folder structure
    organize_folder_structure.delay(source, target, ext)