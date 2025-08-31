# 代码生成时间: 2025-08-31 20:41:03
import os
from celery import Celery
from celery import shared_task
import random
import string

# 定义Celery应用
app = Celery('test_data_generator', broker='pyamqp://guest@localhost//')


# 生成随机测试数据的任务
@app.task
def generate_random_data(length=10):
    """
    生成指定长度的随机测试数据字符串

    :param length: 数据字符串的长度，默认为10
    :return: 随机生成的字符串
    """
    try:
        # 生成随机字符串
        data = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
        # 返回生成的测试数据
        return data
    except Exception as e:
        # 如果发生错误，记录错误信息并抛出异常
        print(f"Error generating random data: {e}")
        raise


# 如果这个脚本被直接运行，则执行测试代码
if __name__ == '__main__':
    # 测试生成随机数据
    try:
        test_data = generate_random_data(length=20)
        print(f"Generated Test Data: {test_data}")
    except Exception as e:
        print(f"Failed to generate test data: {e}")