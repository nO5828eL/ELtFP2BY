# 代码生成时间: 2025-08-31 13:34:42
import os
from celery import Celery
from celery.utils.log import get_task_logger
from urllib.request import urlopen, URLError
import time

# 初始化Celery App
app = Celery('network_status_checker', broker='pyamqp://guest@localhost//')
logger = get_task_logger(__name__)


# 定义检查网络连接的任务
@app.task(bind=True, name='network_status.check_connection')
def check_connection(self, url):
    """
    检查给定URL的网络连接状态的任务。

    参数:
    url (str): 需要检查的URL地址。

    返回:
    tuple: 包含状态码和消息的元组。
    """
    try:
        # 尝试打开URL检查连接
        response = urlopen(url, timeout=10)
        status_code = response.getcode()
        response.close()
        return (200, f'Connection successful to {url}. Status code: {status_code}')
    except URLError as e:
        # 处理URL打开时的错误
        logger.error(f'Failed to connect to {url}. Error: {e.reason}')
        return (503, f'Failed to connect to {url}. Error: {e.reason}')
    except Exception as e:
        # 处理其他异常
        logger.error(f'An unexpected error occurred: {e}')
        return (500, 'An unexpected error occurred.')

# 可选：如果需要在本地脚本中运行检查而不是作为任务
if __name__ == '__main__':
    url_to_check = 'http://example.com'  # 替换为需要检查的URL
    result = check_connection.delay(url_to_check)
    while not result.ready():
        time.sleep(1)  # 等待任务完成
    print(result.get())  # 输出检查结果