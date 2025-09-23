# 代码生成时间: 2025-09-24 00:52:51
import os
import shutil
from celery import Celery
from celery.exceptions import Reject

# 配置Celery
app = Celery('file_backup_sync', broker='pyamqp://guest@localhost//')

# 备份文件函数
def backup_file(source_path, backup_path):
    """
    备份文件到指定路径
    :param source_path: 源文件路径
    :param backup_path: 备份文件路径
    :return: None
    """
    try:
        # 确保源文件存在
        if not os.path.exists(source_path):
            raise FileNotFoundError(f"源文件 {source_path} 不存在")

        # 创建备份目录
        os.makedirs(os.path.dirname(backup_path), exist_ok=True)

        # 备份文件
        shutil.copy2(source_path, backup_path)
        print(f"文件 {source_path} 已备份到 {backup_path}")

    except Exception as e:
        # 记录错误日志
        print(f"备份文件时发生错误：{e}")

# 同步文件函数
def sync_file(source_path, target_path):
    """
    同步源文件到目标路径
    :param source_path: 源文件路径
    :param target_path: 目标文件路径
    :return: None
    """
    try:
        # 确保源文件存在
        if not os.path.exists(source_path):
            raise FileNotFoundError(f"源文件 {source_path} 不存在")

        # 创建目标目录
        os.makedirs(os.path.dirname(target_path), exist_ok=True)

        # 同步文件
        shutil.copy2(source_path, target_path)
        print(f"文件 {source_path} 已同步到 {target_path}")

    except Exception as e:
        # 记录错误日志
        print(f"同步文件时发生错误：{e}")

# Celery任务 - 备份并同步文件
@app.task(bind=True)
def backup_and_sync(self, source_path, backup_path, target_path):
    """
    备份并同步文件
    :param self: Celery任务对象
    :param source_path: 源文件路径
    :param backup_path: 备份文件路径
    :param target_path: 目标文件路径
    :return: None
    """
    try:
        # 备份文件
        backup_file(source_path, backup_path)

        # 同步文件
        sync_file(source_path, target_path)

    except FileNotFoundError as e:
        # 拒绝任务
        self.retry(exc=e)
    except Exception as e:
        # 记录错误日志
        print(f"备份并同步文件时发生错误：{e}")

# 示例用法
if __name__ == '__main__':
    source_path = '/path/to/source/file.txt'
    backup_path = '/path/to/backup/file.txt'
    target_path = '/path/to/target/file.txt'

    # 启动Celery worker
    app.start()

    # 调用备份并同步文件任务
    backup_and_sync.delay(source_path, backup_path, target_path)
