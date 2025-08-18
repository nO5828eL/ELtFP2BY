# 代码生成时间: 2025-08-18 12:13:07
import os
import re
from celery import Celery
from celery.utils.log import get_task_logger

# 初始化Celery
app = Celery('log_parser', broker='pyamqp://guest@localhost//')
app.conf.update(
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    timezone='UTC',
    enable_utc=True,
)
task_logger = get_task_logger(__name__)

# 正则表达式字典，用于匹配不同类型的日志条目
log_patterns = {
    'error': re.compile(r'\[ERROR\] .*'),
    'warning': re.compile(r'\[WARNING\] .*'),
    'info': re.compile(r'\[INFO\] .*'),
}

def parse_log_line(line):
    """
    解析单个日志行，返回匹配的日志级别和消息。
    """
    for level, pattern in log_patterns.items():
        if pattern.search(line):
            return level, line
    return None, line

def parse_log_file(file_path):
    """
    解析整个日志文件，返回所有匹配的日志条目及其级别。
    """
    try:
        with open(file_path, 'r') as file:
            for line in file:
                level, message = parse_log_line(line.strip())
                if level:
                    yield level, message
    except FileNotFoundError:
        task_logger.error(f'Log file not found: {file_path}')
        raise
    except Exception as e:
        task_logger.error(f'An error occurred while parsing the log file: {str(e)}')
        raise

def log_parser_task(file_path):
    """
    Celery任务，用于解析日志文件并存储结果。
    """
    try:
        for level, message in parse_log_file(file_path):
            task_logger.info(f'Parsed log entry: {level} - {message}')
    except Exception as e:
        task_logger.error(f'Error parsing log file: {file_path}. Error: {str(e)}')
    return 'Log file parsed successfully'

# 定义Celery任务
@app.task
def parse_log(file_path):
    "