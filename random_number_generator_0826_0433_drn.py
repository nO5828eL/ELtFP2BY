# 代码生成时间: 2025-08-26 04:33:23
import os
import random
from celery import Celery

# 设置Celery
os.environ.setdefault('CELERY_BROKER_URL', 'amqp://')
app = Celery('random_number_generator', broker='amqp://')

@app.task(bind=True, name='generate_random_number')
def generate_random_number(self, max_value=100, min_value=1):
    """Generates a random number within the specified range.

    Args:
        self (task): The Celery task instance.
        max_value (int): The upper bound of the random number (inclusive).
        min_value (int): The lower bound of the random number (inclusive).

    Returns:
        int: A random number within the specified range.

    Raises:
        ValueError: If max_value is less than min_value.
    """
    if max_value < min_value:
        raise ValueError("max_value must be greater than or equal to min_value")
    return random.randint(min_value, max_value)

# Example usage:
if __name__ == '__main__':
    try:
        result = generate_random_number.delay(100, 1)
        print(f"Generated random number: {result.get()}")
    except Exception as e:
        print(f"An error occurred: {e}")