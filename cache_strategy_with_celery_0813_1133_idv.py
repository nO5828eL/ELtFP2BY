# 代码生成时间: 2025-08-13 11:33:32
import os
from celery import Celery
from celery.exceptions import SoftTimeLimitExceeded
from functools import wraps

# 配置Celery
os.environ.setdefault('CELERY_BROKER_URL', 'amqp://guest@localhost//')
app = Celery('tasks')
app.conf.broker_url = os.environ.get('CELERY_BROKER_URL')
app.conf.result_backend = os.environ.get('CELERY_RESULT_BACKEND')

# 缓存装饰器
def cache(key_prefix, timeout=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cache_key = f"{key_prefix}({args}, {kwargs})"
            # 尝试从缓存中获取结果
            result = app.backend.get(cache_key)
            if result is not None:
                return result
            else:
                try:
                    # 如果缓存中没有，则执行函数并将结果缓存
                    result = func(*args, **kwargs)
                    if timeout is not None:
                        app.backend.set(cache_key, result, timeout)
                    return result
                except SoftTimeLimitExceeded:
                    # 超时异常处理
                    raise ValueError("Function execution exceeded the soft time limit.")
        return wrapper
    return decorator

# 缓存任务
@app.task
@cache(key_prefix="expensive_calculation", timeout=300)  # 缓存5分钟
def expensive_calculation(param1, param2):
    """
    模拟一个耗时的操作，例如复杂的数学计算
    """
    # 模拟耗时操作
    import time
    time.sleep(2)  # 模拟2秒的延时
    result = param1 + param2
    return result

# 错误处理
@app.task(bind=True)
def handle_timeout(self):
    """
    如果任务超时，可以在这里处理
    """
    try:
        result = expensive_calculation(4, 5)
    except SoftTimeLimitExceeded:
        self.retry(exc=SoftTimeLimitExceeded(), countdown=60)  # 1分钟后重试
        return None
    return result

if __name__ == '__main__':
    app.start()