# 代码生成时间: 2025-08-12 07:57:56
from celery import Celery
from celery.exceptions import SoftTimeLimitExceeded
import os
import shutil
import logging
from datetime import datetime

# 配置Celery
app = Celery('data_backup_recover',
             broker='amqp://guest@localhost//',
             backend='rpc://')

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.task(soft_time_limit=60)  # 设置任务超时时间
def backup_data(source_path, backup_path):
    """
    备份数据的函数
    :param source_path: 源数据路径
    :param backup_path: 备份数据路径
    :return: None
    """
    try:
        # 生成备份文件的名称
        backup_file_name = f"{os.path.basename(source_path)}_{datetime.now().strftime('%Y%m%d%H%M%S')}.bak"
        full_backup_path = os.path.join(backup_path, backup_file_name)
        
        # 执行备份操作
        shutil.copy2(source_path, full_backup_path)
        logger.info(f"Backup successful: {source_path} -> {full_backup_path}")
    except Exception as e:
        logger.error(f"Backup failed: {e}")
        raise e

@app.task(soft_time_limit=60)  # 设置任务超时时间
def recover_data(backup_path, target_path):
    """
    恢复数据的函数
    :param backup_path: 备份文件路径
    :param target_path: 目标恢复路径
    :return: None
    """
    try:
        # 执行恢复操作
        for file in os.listdir(backup_path):
            if file.endswith('.bak'):
                source = os.path.join(backup_path, file)
                target = os.path.join(target_path, os.path.basename(file).split('.')[0])
                shutil.copy2(source, target)
                logger.info(f"Recover successful: {source} -> {target}")
    except Exception as e:
        logger.error(f"Recover failed: {e}")
        raise e

if __name__ == '__main__':
    # 测试备份和恢复功能
    source = '/path/to/source/directory'
    backup = '/path/to/backup/directory'
    target = '/path/to/target/directory'
    
    # 执行备份任务
    backup_data.delay(source, backup)
    
    # 执行恢复任务
    recover_data.delay(backup, target)