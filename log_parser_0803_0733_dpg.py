# 代码生成时间: 2025-08-03 07:33:37
import os
import re
from celery import Celery
from celery.result import allow_join_result

# 配置Celery
app = Celery('log_parser', broker='pyamqp://guest@localhost//')

# 定义一个正则表达式用于解析日志文件
LOG_PATTERN = re.compile(r'\[(.*?)\] (.*?): (.*)')

# 定义一个任务来解析单个日志文件
@app.task(bind=True)
def parse_log_file(self, file_path):
    """
    解析日志文件并提取信息。
    
    :param self: Celery任务实例
    :param file_path: 日志文件的路径
    :return: 解析后的日志信息列表
    """
    results = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                match = LOG_PATTERN.search(line)
                if match:
                    # 提取日志时间、级别和消息
                    log_time, log_level, log_message = match.groups()
                    results.append({'time': log_time, 'level': log_level, 'message': log_message.strip()})
    except FileNotFoundError:
        raise self.retry(exc=FileNotFoundError('Log file not found'))
    except Exception as e:
        raise self.retry(exc=e)
    return results

# 定义一个任务来处理多个日志文件
@app.task
def parse_multiple_log_files(file_paths):
    """
    处理多个日志文件。
    
    :param file_paths: 日志文件路径列表
    :return: 所有日志文件解析结果的列表
    """
    results = []
    for file_path in file_paths:
        result = parse_log_file.delay(file_path)
        results.append(result)
    return allow_join_result(results)

# 主函数，用于测试和演示
if __name__ == '__main__':
    # 假设有两个日志文件路径
    log_files = ['/path/to/logfile1.log', '/path/to/logfile2.log']
    # 解析日志文件
    results = parse_multiple_log_files(log_files)
    for result in results:
        print(result.get())
