# 代码生成时间: 2025-09-02 21:08:13
import json
from celery import Celery, shared_task

# 配置 Celery
app = Celery('json_converter',
             broker='pyamqp://guest@localhost//')


# JSON数据格式转换器任务
@shared_task(bind=True, default_retry_delay=10, max_retries=3)
def json_converter_task(self, input_data):
    """
    This task is designed to convert a JSON input into a
    different format. The task will catch exceptions
    to ensure that it can retry in case of failures.
    
    :param self: The Celery task self reference
    :param input_data: The input JSON data to be converted
    :return: The converted JSON data or an error message
    """
    try:
        # Parse the input JSON data
        input_json = json.loads(input_data)

        # Perform the conversion logic here
        # For demonstration purposes, we will just convert the JSON back to a string
        output_json = json.dumps(input_json, indent=4)

        # Return the converted JSON data
        return {"status": "success", "data": output_json}
    except json.JSONDecodeError as e:
        # Handle JSON parsing errors
        return {"status": "error", "message": str(e)}
    except Exception as e:
        # Handle any other exceptions that may occur
        return {"status": "error", "message": str(e)}


# Example usage of the decorator
@app.task(base=json_converter_task)
def convert_json(input_data):
    """
    This function serves as an entry point for converting JSON data.
    It will call the json_converter_task function and handle any
    exceptions that might occur during the execution of the task.
    
    :param input_data: The input JSON data to be converted
    :return: The result of the json_converter_task
    """
    return json_converter_task.delay(input_data=input_data)
