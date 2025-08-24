# 代码生成时间: 2025-08-24 17:21:56
import os
import csv
from celery import Celery
from celery.utils.log import get_task_logger
from openpyxl import Workbook

# Configure the logger
logger = get_task_logger(__name__)

# Initialize Celery
app = Celery('excel_generator',
             broker='amqp://guest@localhost//',
             backend='rpc://')
app.conf.update(
    result_expires=3600,
)

# Define the task for generating Excel files
@app.task(name='excel_generator.generate', bind=True)
def generate_excel(self, data, filename_prefix):
    """
    Generate an Excel file based on provided data.

    :param data: List of dictionaries where each dictionary represents a row in the Excel file.
    :param filename_prefix: The prefix for the Excel file name.
    """
    try:
        # Create a new Excel workbook
        wb = Workbook()
        ws = wb.active
        ws.title = 'Data'

        # Assuming data is a list of dictionaries with the same structure
        if data:
            # Write headers based on the keys of the first dictionary
            headers = list(data[0].keys())
            ws.append(headers)
            # Write data rows
            for row in data:
                ws.append(list(row.values()))
        else:
            logger.warning('No data provided to generate Excel file.')
            return

        # Save the Excel file
        filename = f"{filename_prefix}.xlsx"
        wb.save(filename=filename)
        logger.info(f'Excel file generated successfully: {filename}')
        return filename
    except Exception as e:
        logger.error(f'Failed to generate Excel file: {e}')
        raise

# Example usage
if __name__ == '__main__':
    # Sample data to generate an Excel file
    data = [
        {'Name': 'John', 'Age': 30, 'City': 'New York'},
        {'Name': 'Alice', 'Age': 28, 'City': 'Los Angeles'},
    ]
    filename_prefix = 'Generated_Excel'
    generate_excel.delay(data, filename_prefix)