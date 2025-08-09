# 代码生成时间: 2025-08-10 03:02:34
import hashlib
from celery import Celery
from celery import shared_task

# 配置Celery
app = Celery('hash_calculator', broker='pyamqp://guest@localhost//')


# 哈希值计算任务
@shared_task
def calculate_hash(input_data):
    """
    计算输入数据的哈希值。

    参数:
    input_data (str): 待计算哈希值的字符串。

    返回:
    str: 计算得到的哈希值。

    异常:
    ValueError: 如果输入数据不是字符串。
    """
    if not isinstance(input_data, str):
        raise ValueError("输入数据必须是字符串。")

    # 使用SHA-256算法计算哈希值
    hash_object = hashlib.sha256(input_data.encode())
    hash_value = hash_object.hexdigest()

    return hash_value


# 以下代码用于本地测试，实际部署时不需要
if __name__ == '__main__':
    # 测试哈希值计算任务
    test_data = 'Hello, World!'
    result = calculate_hash(test_data)
    print(f'输入数据: {test_data}')
    print(f'哈希值: {result}')
