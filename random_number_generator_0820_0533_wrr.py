# 代码生成时间: 2025-08-20 05:33:17
import os
import random
from celery import Celery

# 配置Celery
app = Celery('random_number_generator', broker='pyamqp://guest@localhost//')

@app.task
def generate_random_number(min_value, max_value):
    """
    生成一个介于min_value和max_value之间的随机数。
    
    参数:
    min_value (int): 随机数的最小值。
    max_value (int): 随机数的最大值。
    
    返回:
    int: 一个随机数。
    
    异常:
    ValueError: 如果min_value大于max_value。
    """
    # 检查min_value是否小于等于max_value
    if min_value > max_value:
        raise ValueError("min_value should not be greater than max_value")
    
    # 生成一个随机数并返回
    return random.randint(min_value, max_value)

# 设置环境变量
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')

# 以下代码用于测试和演示目的，不应包含在生产代码中
if __name__ == '__main__':
    try:
        # 调用任务生成随机数
        result = generate_random_number.delay(1, 10)
        # 等待任务完成
        print(f"Random number generated: {result.get()}")
    except ValueError as e:
        print(f"Error: {e}")