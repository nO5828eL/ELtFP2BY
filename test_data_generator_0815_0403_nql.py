# 代码生成时间: 2025-08-15 04:03:20
import csv
from celery import Celery
from celery.utils.log import get_task_logger

# 配置Celery
app = Celery('test_data_generator', broker='pyamqp://guest@localhost//')

# 获取Celery的logger
logger = get_task_logger(__name__)

@app.task(bind=True)
def generate_test_data(self, data_rows):
    """
    异步任务：生成测试数据并写入CSV文件
    
    参数:
    data_rows (list): 一个包含测试数据行的列表
    
    返回:
    str: CSV文件路径
    
    异常:
    Exception: 如果文件写入失败
    """
    try:
        # 定义CSV文件路径
        file_path = 'test_data.csv'
        
        # 打开文件并写入数据
        with open(file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            # 写入表头
            writer.writerow(['ID', 'Name', 'Email', 'Phone'])
            
            # 写入数据行
            for row in data_rows:
                writer.writerow(row)
                
        # 记录日志
        logger.info(f'Test data generated successfully: {file_path}')
        
        # 返回文件路径
        return file_path
    
    except Exception as e:
        # 记录异常日志
        logger.error(f'Failed to generate test data: {str(e)}')
        
        # 重新抛出异常
        raise

# 示例用法
if __name__ == '__main__':
    # 示例测试数据
    test_data = [
        [1, 'John Doe', 'john.doe@example.com', '123-456-7890'],
        [2, 'Jane Doe', 'jane.doe@example.com', '987-654-3210'],
    ]
    
    # 调用异步任务
    result = generate_test_data.delay(test_data)
    
    # 获取结果
    file_path = result.get()
    print(f'Test data generated at: {file_path}')
