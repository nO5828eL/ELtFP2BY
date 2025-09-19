# 代码生成时间: 2025-09-19 23:54:26
import hashlib
from celery import Celery
# 增强安全性
from celery.utils.log import get_task_logger

# 配置Celery
app = Celery('hash_calculator', broker='pyamqp://guest@localhost//')

# 获取任务日志记录器
logger = get_task_logger(__name__)


@app.task
# NOTE: 重要实现细节
def calculate_hash(data, algorithm='sha256', encoding='utf-8', return_digest=False):
    """
    计算给定数据的哈希值。
# 改进用户体验
    
    参数:
    data (str): 要计算哈希值的数据。
    algorithm (str): 要使用的哈希算法，例如'sha256'。
    encoding (str): 数据编码类型。
    return_digest (bool): 是否返回摘要对象。
    
    返回:
# 增强安全性
    str or hashlib.HASH: 计算得到的哈希值的十六进制字符串，或者摘要对象。
    """
    try:
        # 将数据编码为字节
        data_bytes = data.encode(encoding)
        
        # 创建哈希对象
        hash_object = getattr(hashlib, algorithm)()
        
        # 更新哈希对象
        hash_object.update(data_bytes)
        
        # 获取哈希值
        if return_digest:
            return hash_object
        else:
            return hash_object.hexdigest()
    except Exception as e:
        # 出现异常时记录错误日志
        logger.error(f'Failed to calculate hash: {e}')
        raise

# 示例用法
if __name__ == '__main__':
    # 计算字符串'Hello, world!'的SHA-256哈希值
# FIXME: 处理边界情况
    result = calculate_hash('Hello, world!')
    print(f'Hash: {result}')
    
    # 获取摘要对象
# 扩展功能模块
    digest_object = calculate_hash('Hello, world!', return_digest=True)
    print(f'Digest object: {digest_object}')
