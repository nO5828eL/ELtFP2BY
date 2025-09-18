# 代码生成时间: 2025-09-19 03:39:35
# test_data_generator.py
# This script generates test data using Celery task queues.

from celery import Celery
from datetime import datetime

# Configure the Celery app
app = Celery('test_data_generator', broker='pyamqp://guest@localhost//')
app.conf.update(
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    timezone='UTC',
    enable_utc=True,
    result_expires=3600
)

def generate_test_data():
    """
    This function generates random test data and returns it.
    The data includes a timestamp and a random string.
    """
    try:
        # Generate a timestamp
        timestamp = datetime.now().isoformat()
        # Generate a random string
        random_string = ''.join([chr(random.choice(range(97, 122))) for _ in range(10)])
        # Return the test data
        return {'timestamp': timestamp, 'random_string': random_string}
    except Exception as e:
        # Handle any exceptions that occur during data generation
        print(f"Error generating test data: {e}")
        raise

@app.task
def generate_and_store_test_data():
    """
    This Celery task generates test data and then stores it.
    It calls the generate_test_data function to get the data and
    then prints it to simulate storage.
    """
    try:
        # Generate the test data
        test_data = generate_test_data()
        # Simulate storing the data (e.g., by printing it)
        print(f"Storing test data: {test_data}")
    except Exception as e:
        # Handle any exceptions that occur during data generation or storage
        print(f"Error storing test data: {e}")
        raise

if __name__ == '__main__':
    # Run the Celery worker to process tasks
    app.start()
