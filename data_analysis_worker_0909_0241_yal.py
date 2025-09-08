# 代码生成时间: 2025-09-09 02:41:46
# data_analysis_worker.py

"""
Data Analysis Worker module using Celery task queue.
This module defines tasks for data analysis.
"""

from celery import Celery
import os

# Configure Celery with Redis backend
os.environ.setdefault('CELERY_BROKER_URL', 'redis://localhost:6379/0')
os.environ.setdefault('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')

app = Celery('data_analysis_worker', broker=os.environ['CELERY_BROKER_URL'],
             backend=os.environ['CELERY_RESULT_BACKEND'])

app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)


@app.task(name='data_analysis_worker.sum_data')
def sum_data(data):
    """
    Calculate the sum of a list of numbers.

    :param data: List of numbers
    :return: Sum of the numbers
    :raises: ValueError if data is not a list or contains non-numeric items
    """
    if not isinstance(data, list):
        raise ValueError('Input data must be a list.')

    try:
        total = sum(data)
    except TypeError:
        raise ValueError('All items in the list must be numbers.')

    return total


@app.task(name='data_analysis_worker.average_data')
def average_data(data):
    """
    Calculate the average of a list of numbers.

    :param data: List of numbers
    :return: Average of the numbers
    :raises: ValueError if data is not a list or contains non-numeric items
    """
    if not isinstance(data, list) or len(data) == 0:
        raise ValueError('Input data must be a non-empty list.')

    try:
        total = sum(data)
        average = total / len(data)
    except TypeError:
        raise ValueError('All items in the list must be numbers.')

    return average


@app.task(name='data_analysis_worker.max_data')
def max_data(data):
    """
    Find the maximum value in a list of numbers.

    :param data: List of numbers
    :return: Maximum number in the list
    :raises: ValueError if data is not a list or contains non-numeric items
    """
    if not isinstance(data, list) or len(data) == 0:
        raise ValueError('Input data must be a non-empty list.')

    try:
        maximum = max(data)
    except ValueError:
        raise ValueError('All items in the list must be numbers.')

    return maximum


@app.task(name='data_analysis_worker.min_data')
def min_data(data):
    """
    Find the minimum value in a list of numbers.

    :param data: List of numbers
    :return: Minimum number in the list
    :raises: ValueError if data is not a list or contains non-numeric items
    """
    if not isinstance(data, list) or len(data) == 0:
        raise ValueError('Input data must be a non-empty list.')

    try:
        minimum = min(data)
    except ValueError:
        raise ValueError('All items in the list must be numbers.')

    return minimum
