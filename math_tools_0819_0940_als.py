# 代码生成时间: 2025-08-19 09:40:28
import math
from celery import Celery

# 配置Celery
app = Celery('math_tools', broker='pyamqp://guest@localhost//')

# 定义数学计算任务
@app.task
def add(x, y):
    """Add two numbers together.

    Args:
        x (int): First number.
        y (int): Second number.

    Returns:
        int: The sum of x and y.
    """
    return x + y

@app.task
def subtract(x, y):
    """Subtract two numbers.

    Args:
        x (int): First number.
        y (int): Second number.

    Returns:
        int: The difference of x and y.
    """
    try:
        result = x - y
    except TypeError:
        raise ValueError("Both numbers must be integers.")
    return result

@app.task
def multiply(x, y):
    """Multiply two numbers.

    Args:
        x (int): First number.
        y (int): Second number.

    Returns:
        int: The product of x and y.
    """
    return x * y

@app.task
def divide(x, y):
    """Divide two numbers.

    Args:
        x (int): First number.
        y (int): Second number.

    Returns:
        float: The quotient of x and y.

    Raises:
        ValueError: If y is zero.
    """
    if y == 0:
        raise ValueError("Cannot divide by zero.")
    return x / y

# 运行Celery worker
if __name__ == '__main__':
    app.start()