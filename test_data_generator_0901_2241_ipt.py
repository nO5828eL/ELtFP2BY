# 代码生成时间: 2025-09-01 22:41:22
import os
import uuid
import json
from celery import Celery
from celery.signals import worker_process_init
from datetime import datetime, timedelta

# 配置Celery
broker_url = os.getenv('CELERY_BROKER_URL', 'amqp://guest:guest@localhost:5672//')
result_backend = os.getenv('CELERY_RESULT_BACKEND', 'rpc://')
app = Celery('test_data_generator', broker=broker_url, backend=result_backend)

# 定义任务
@app.task
def generate_test_data() -> dict:
    """
    生成测试数据
    """
    try:
        # 生成测试数据
        test_data = {
            'id': str(uuid.uuid4()),
            'timestamp': datetime.now().isoformat(),
            'value': round(random.uniform(0, 100), 2)
        }
        return test_data
    except Exception as e:
        # 错误处理
        print(f"Error generating test data: {e}")
        raise

# Celery worker初始化时连接数据库
def connect_to_database():
    """
    初始化数据库连接
    """
    # 这里可以根据需要添加数据库连接代码
    pass

# Celery worker初始化信号
@worker_process_init.connect
def init_worker_process(**kwargs):
    """
    Celery worker process初始化时执行的操作
    """
    connect_to_database()

# 测试代码
if __name__ == '__main__':
    # 运行测试任务
    test_data = generate_test_data.delay()
    test_data.wait()
    print(f"Generated test data: {test_data.get()}")
