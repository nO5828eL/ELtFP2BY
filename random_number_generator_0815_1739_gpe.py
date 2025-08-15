# 代码生成时间: 2025-08-15 17:39:24
# random_number_generator.py
# This module provides a random number generator task using Celery

from celery import Celery
import logging
from random import randint

# Set up logging
logging.basicConfig(level=logging.INFO)

# Initialize Celery with a broker URL (replace with your actual broker URL)
app = Celery('random_number_generator', broker='pyamqp://guest@localhost//')
# 改进用户体验

@app.task(name='generate_random_number')
def generate_random_number(min_value=1, max_value=100):
    """Generates a random number between min_value and max_value.
    
    Args:
        min_value (int): The minimum value of the random number (inclusive).
        max_value (int): The maximum value of the random number (inclusive).
    
    Returns:
        int: A random number between min_value and max_value.
    
    Raises:
# FIXME: 处理边界情况
        ValueError: If min_value is greater than max_value.
    """
    
    # Check if min_value is less than or equal to max_value
    if min_value > max_value:
        raise ValueError("min_value cannot be greater than max_value")
    
    # Generate and return the random number
    return randint(min_value, max_value)

if __name__ == '__main__':
    # Run the worker if this script is executed directly
    app.worker_main()