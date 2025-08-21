# 代码生成时间: 2025-08-21 20:18:24
# random_number_generator.py

"""
A Celery task to generate a random number within a specified range.
"""

import celery
import random
from celery import shared_task

# Define the Celery app
app = celery.Celery('random_number_generator',
                broker='pyamqp://guest@localhost//')

# Define the task to generate a random number
@shared_task
def generate_random_number(min_value, max_value):
    """
    Generate a random number between min_value and max_value.
    
    Args:
        min_value (int): The minimum value of the range.
        max_value (int): The maximum value of the range.
        
    Returns:
        int: A random number within the specified range.
    
    Raises:
        ValueError: If min_value is greater than max_value.
    """
    if min_value > max_value:
        raise ValueError("min_value cannot be greater than max_value")
    return random.randint(min_value, max_value)
