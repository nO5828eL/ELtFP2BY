# 代码生成时间: 2025-08-17 12:03:33
#!/usr/bin/env python

"""
A JSON data format converter using Python and Celery framework.
"""

import json
from celery import Celery
from celery.exceptions import SoftTimeLimitExceeded

# Configuration for Celery
app = Celery('json_transformer', broker='pyamqp://guest@localhost//')
app.conf.task_soft_time_limit = 10  # seconds
app.conf.task_time_limit = 15  # seconds


@app.task(bind=True)
def convert_json(self, input_data, target_format):
    """
    Converts the input JSON data to the specified target format.

    :param self: The task instance.
    :param input_data: The JSON data to be converted.
    :param target_format: The target format of the JSON data.
    :raises ValueError: If the input data is invalid or the target format is unsupported.
    :return: The converted JSON data in the specified target format.
    """
    try:
        # Load the input data as JSON
        data = json.loads(input_data)

        # Check if the target format is supported
        if target_format not in ['compact', 'pretty']:
            raise ValueError(f'Unsupported target format: {target_format}')

        # Convert the data to the target format
        if target_format == 'compact':
            result = json.dumps(data)
        elif target_format == 'pretty':
            result = json.dumps(data, indent=4)
        else:
            raise ValueError(f'Unexpected target format: {target_format}')

        return result

    except json.JSONDecodeError as e:
        # Handle JSON decoding errors
        raise ValueError(f'Invalid JSON input: {e}') from e

    except SoftTimeLimitExceeded:
        # Handle task timeouts
        raise ValueError('Task timed out while converting JSON data') from None

# Example usage:
if __name__ == '__main__':
    # Define example input data and target format
    input_data = '''{
        "key": "value",
        "nested": {
            "inner_key": "inner_value"
        }
    }'''
    target_format = 'pretty'

    # Run the conversion task
    try:
        result = convert_json.delay(input_data, target_format)
        print(result.get())
    except ValueError as e:
        print(f'Error: {e}')
