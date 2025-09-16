# 代码生成时间: 2025-09-16 19:09:55
import os
import uuid
from celery import Celery
from celery.result import AsyncResult
import logging

# 设置日志配置
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 配置Celery
app = Celery('data_generator',
             broker='amqp://',  # 使用默认的RabbitMQ配置
             backend='rpc://')

# 定义数据生成任务
@app.task
def generate_data(dataset_size):
    """
    生成指定数量的测试数据
    :param dataset_size: int - 数据集的大小
    :return: str - 数据集的唯一标识
    """
    try:
        data_set = []
        for _ in range(dataset_size):
            # 生成每个数据项，这里示例使用UUID作为数据
            new_id = str(uuid.uuid4())
            data_set.append(new_id)
            # 模拟数据处理时间
            time.sleep(0.01)
        # 将数据集保存到文件
        dataset_id = str(uuid.uuid4())
        filename = f'{dataset_id}.txt'
        with open(filename, 'w') as file:
            file.write('
'.join(data_set))
        logger.info(f'Data set generated with ID: {dataset_id} and size: {len(data_set)}')
        return filename
    except Exception as e:
        logger.error(f'Error generating data set: {e}')
        raise

# 以下为测试和使用示例
if __name__ == '__main__':
    try:
        # 启动Celery worker
        app.start()
        # 调用异步任务
        result = generate_data.delay(100)
        # 等待任务完成并获取结果
        data_file = result.get(timeout=60)
        print(f'Generated data file: {data_file}')
    except Exception as e:
        logger.error(f'Error in main execution: {e}')
    finally:
        # 确保关闭worker
        app.control.stop()
