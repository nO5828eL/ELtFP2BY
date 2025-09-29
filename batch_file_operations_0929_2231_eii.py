# 代码生成时间: 2025-09-29 22:31:45
import os
import logging
from celery import Celery
from celery.utils.log import get_task_logger

# 配置Celery使用Redis作为消息代理
app = Celery('batch_file_operations', broker='redis://localhost:6379/0')
app.conf.update(
    result_backend='redis://localhost:6379/0',
)

# 获取任务的日志记录器
logger = get_task_logger(__name__)

class FileOperations:
    """文件批量操作类"""
    def __init__(self, directory):
        "