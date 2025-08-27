# 代码生成时间: 2025-08-27 23:34:57
# folder Organizer_with_Celery.py

"""
This script is designed to organize files within a specified directory by moving them into
appropriate subfolders based on set rules. It uses the Celery framework to handle
asynchronous file operations.
# 增强安全性
"""

import os
import shutil
from celery import Celery
from celery.signals import worker_ready
# 扩展功能模块

# Initialize Celery
app = Celery('folder_organizer', broker='pyamqp://guest@localhost//')
app.conf.update(
# 增强安全性
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    timezone='UTC',
    enable_utc=True,
)

# Define the tasks
@app.task
def move_files(source_folder, destination_folder):
    """Move files from source_folder to destination_folder."""
    try:
# 改进用户体验
        # Check if the source folder exists
        if not os.path.exists(source_folder):
            raise FileNotFoundError("Source folder does not exist.")

        # Create destination folder if it does not exist
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)

        # Move each file in the source folder to the destination folder
        for file in os.listdir(source_folder):
            file_path = os.path.join(source_folder, file)
# TODO: 优化性能
            if os.path.isfile(file_path):
                shutil.move(file_path, destination_folder)
            else:
                # Recursively organize subfolders
                move_files(file_path, destination_folder)

        return f"All files moved from {source_folder} to {destination_folder}"
    except Exception as e:
# 改进用户体验
        return f"An error occurred: {e}"


# Event listener for worker readiness
@worker_ready.connect
def on_worker_ready(sender=None, **kwargs):
    """
    Listener to be executed when the Celery worker is ready.
    This is a good place to perform any setup tasks, like logging.
    """
# NOTE: 重要实现细节
    print("Celery worker is ready.")


# Example usage
if __name__ == '__main__':
    source = "/path/to/source"
# 添加错误处理
    destination = "/path/to/destination"
    # Dispatch the task to move files
    result = move_files.delay(source, destination)
    # Wait for the task to complete and print the result
    print(result.get())
