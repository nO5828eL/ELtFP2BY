# 代码生成时间: 2025-09-13 09:35:07
# -*- coding: utf-8 -*-

"""
File Backup and Synchronization Tool using Python and Celery.
This script is designed to backup and synchronize files between two locations.
"""

import os
import shutil
from celery import Celery
from celery.exceptions import SoftTimeLimitExceeded

# Define the broker and backend for Celery
celery_app = Celery(
    'file_backup_synchronizer',
    broker='pyamqp://guest@localhost//',
    backend='rpc://'
)


@celery_app.task
def backup_file(source_path, destination_path):
    """
    Backs up a file from the source path to the destination path.

    Args:
        source_path (str): The path to the source file.
        destination_path (str): The path to the destination file.

    Returns:
        str: A message indicating the status of the backup operation.
    """
    try:
        # Ensure the destination directory exists
        os.makedirs(os.path.dirname(destination_path), exist_ok=True)

        # Copy the file from source to destination
        shutil.copy2(source_path, destination_path)
        return f"Backup successful: {source_path} -> {destination_path}"
    except Exception as e:
        return f"Backup failed: {e}"


@celery_app.task
def synchronize_files(source_dir, destination_dir):
    """
    Synchronizes files between two directories.

    Args:
        source_dir (str): The path to the source directory.
        destination_dir (str): The path to the destination directory.

    Returns:
        str: A message indicating the status of the synchronization operation.
    """
    try:
        # Ensure the destination directory exists
        os.makedirs(destination_dir, exist_ok=True)

        # Iterate over files in the source directory and synchronize them
        for filename in os.listdir(source_dir):
            source_file_path = os.path.join(source_dir, filename)
            destination_file_path = os.path.join(destination_dir, filename)

            # Skip directories
            if os.path.isdir(source_file_path):
                continue

            # Copy the file if it doesn't exist in the destination or is newer
            if not os.path.exists(destination_file_path) or \
               os.path.getmtime(source_file_path) > os.path.getmtime(destination_file_path):
                backup_file.apply_async((source_file_path, destination_file_path))

        return "Synchronization completed successfully"
    except Exception as e:
        return f"Synchronization failed: {e}"


if __name__ == '__main__':
    # Example usage of the backup_file and synchronize_files tasks
    print(backup_file('path/to/source/file.txt', 'path/to/destination/file.txt'))
    print(synchronize_files('path/to/source/directory', 'path/to/destination/directory'))