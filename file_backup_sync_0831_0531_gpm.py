# 代码生成时间: 2025-08-31 05:31:13
# file_backup_sync.py
# A simple file backup and synchronization tool using Python and Celery.

import os
import shutil
from celery import Celery
from celery import shared_task
from celery.exceptions import SoftTimeLimitExceeded

app = Celery('file_backup_sync', broker='pyamqp://guest@localhost//')

# Configuration settings for synchronization
BACKUP_SOURCE = '/path/to/source/directory'
BACKUP_DESTINATION = '/path/to/destination/directory'

@app.task(bind=True, soft_time_limit=60)
def backup_and_sync(self, source, destination):
    """
    A Celery task to backup and synchronize files from source to destination.
    :param self: Celery task instance
    :param source: The source directory to backup
    :param destination: The destination directory for the backup
    :return: None
    """
    try:
        # Check if the source and destination directories exist
        if not os.path.exists(source):
            raise FileNotFoundError(f"The source directory {source} does not exist.")
        if not os.path.exists(destination):
            os.makedirs(destination)
            print(f"Destination directory {destination} created.")

        # Synchronize files from source to destination
        for item in os.listdir(source):
            source_path = os.path.join(source, item)
            destination_path = os.path.join(destination, item)

            # Check if the item is a file and not a directory
            if os.path.isfile(source_path):
                # If the file does not exist in destination, copy it
                if not os.path.exists(destination_path):
                    shutil.copy2(source_path, destination_path)
                    print(f"Copied {source_path} to {destination_path}.")
                # If the file exists in destination, update if it's newer
                elif os.path.getmtime(source_path) > os.path.getmtime(destination_path):
                    shutil.copy2(source_path, destination_path)
                    print(f"Updated {destination_path} with {source_path}.")

    except SoftTimeLimitExceeded:
        self.retry(exc=TimeoutError("Task exceeded the soft time limit."))
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage:
# backup_and_sync.apply_async(args=(BACKUP_SOURCE, BACKUP_DESTINATION))
