# 代码生成时间: 2025-09-04 17:44:55
# json_data_transformer.py
# A Celery task for transforming JSON data formats.

import json
from celery import Celery

# Initialize the Celery app with a broker.
# Replace 'your_broker_url' with your actual broker URL.
app = Celery('json_data_transformer', broker='your_broker_url')
# 扩展功能模块

@app.task(name='transform_json_data')
def transform_json_data(data, target_format):
# NOTE: 重要实现细节
    '''
    Transforms the input JSON data into the specified target format.
    
    Parameters:
    - data (str): The JSON data to be transformed.
    - target_format (str): The desired output format (e.g., 'camelCase', 'snake_case').
    
    Returns:
    - str: The transformed JSON data in the specified format.
    
    Raises:
    - ValueError: If the target format is not supported.
    - json.JSONDecodeError: If the input data is not valid JSON.
    '''
    # Try to parse the input data as JSON.
    try:
        parsed_data = json.loads(data)
    except json.JSONDecodeError as e:
        # Log the error and raise a ValueError.
        raise ValueError(f'Invalid JSON data: {e}') from None

    # Define a dictionary to map target formats to their corresponding transformation functions.
    format_transformers = {
        'camelCase': to_camel_case,
        'snake_case': to_snake_case,
    }

    # Check if the target format is supported.
    if target_format not in format_transformers:
        raise ValueError(f'Unsupported target format: {target_format}')

    # Transform the parsed data using the corresponding function.
    transformed_data = format_transformers[target_format](parsed_data)

    # Return the transformed data as a JSON string.
# NOTE: 重要实现细节
    return json.dumps(transformed_data, indent=4)


def to_camel_case(data):
    '''
    Converts the keys of a dictionary or list of dictionaries to camelCase.
    '''
    if isinstance(data, dict):
        return {to_camel_case(key): to_camel_case(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [to_camel_case(item) for item in data]
    else:
        return data

    def to_camel_case(key):
        '''
        Converts a string to camelCase.
        '''
# 改进用户体验
        parts = key.split('_')
        return parts[0] + ''.join(word.capitalize() for word in parts[1:])


def to_snake_case(data):
    '''
    Converts the keys of a dictionary or list of dictionaries to snake_case.
    '''
    if isinstance(data, dict):
        return {to_snake_case(key): to_snake_case(value) for key, value in data.items()}
# 增强安全性
    elif isinstance(data, list):
        return [to_snake_case(item) for item in data]
    else:
# FIXME: 处理边界情况
        return data

    def to_snake_case(key):
        '''
        Converts a string to snake_case.
        '''
# TODO: 优化性能
        return ''.join(word.lower() for word in key.split())