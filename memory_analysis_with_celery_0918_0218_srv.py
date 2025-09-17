# 代码生成时间: 2025-09-18 02:18:42
import os
import psutil
from celery import Celery

# 配置Celery
app = Celery('memory_analysis', broker='pyamqp://guest@localhost//')

# 定义一个Celery任务来分析内存使用情况
@app.task
def analyze_memory_usage():
    """
    分析当前系统的内存使用情况。
    
    返回值：
        memory_info: 一个字典，包含内存使用的详细信息。
    """
    try:
        # 获取内存使用信息
        memory = psutil.virtual_memory()
        
        # 构建内存使用信息字典
        memory_info = {
            'total': memory.total,
            'available': memory.available,
            'used': memory.used,
            'free': memory.free,
            'percent': memory.percent,
        }
        
        # 返回内存使用信息
        return memory_info
        
    except Exception as e:
        # 错误处理
        print(f"An error occurred: {e}")
        return None

# 以下代码用于测试任务功能是否正常
if __name__ == '__main__':
    result = analyze_memory_usage.delay()
    print(f"Memory analysis result: {result.get(timeout=10)}")
