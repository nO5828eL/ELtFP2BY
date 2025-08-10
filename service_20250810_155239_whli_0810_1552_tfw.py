# 代码生成时间: 2025-08-10 15:52:39
import os
import shutil
from celery import Celery
from celery.utils.log import get_task_logger

# 配置Celery
app = Celery('folder_structure_organizer',
             broker='pyamqp://guest@localhost//')
app.conf.update(task_serializer='json',
                 accept_content=['json'],
                 result_serializer='json',
                 timezone='UTC',
                 enable_utc=True)

# 获取Celery的日志记录器
logger = get_task_logger(__name__)

# 任务：整理文件夹结构
@app.task(name='organize_folder_structure')
def organize_folder_structure(target_folder,
                              destination_folder,
                              file_types_to_move=None):
    """
    移动指定类型文件到目标文件夹中
    :param target_folder: 需要整理的文件夹路径
    :param destination_folder: 目标文件夹路径
    :param file_types_to_move: 需要移动的文件类型列表，例如：['.jpg', '.png']
    :return: None
    """
    try:
        # 检查目标文件夹是否存在
        if not os.path.exists(target_folder):
            logger.error(f'目标文件夹不存在: {target_folder}')
            raise FileNotFoundError(f'目标文件夹不存在: {target_folder}')

        # 检查目标文件夹是否为文件夹
        if not os.path.isdir(target_folder):
            logger.error(f'目标路径不是文件夹: {target_folder}')
            raise NotADirectoryError(f'目标路径不是文件夹: {target_folder}')

        # 创建目标文件夹，如果不存在
        os.makedirs(destination_folder, exist_ok=True)

        # 遍历目标文件夹中的所有文件
        for filename in os.listdir(target_folder):
            # 获取文件的完整路径
            file_path = os.path.join(target_folder, filename)

            # 检查是否为文件
            if os.path.isfile(file_path):
                # 如果file_types_to_move为空，则移动所有文件，否则只移动指定类型的文件
                if file_types_to_move is None or \
                        os.path.splitext(filename)[1].lower() in file_types_to_move:
                    # 移动文件
                    shutil.move(file_path, destination_folder)
                    logger.info(f'文件 {filename} 已移动到 {destination_folder}')

    except FileNotFoundError as e:
        logger.error(e)
    except NotADirectoryError as e:
        logger.error(e)
    except Exception as e:
        logger.error(f'整理文件夹结构时出现错误: {e}')

# 示例用法
if __name__ == '__main__':
    # 定义需要整理的文件夹路径和目标文件夹路径
    target_folder = '/path/to/source'
    destination_folder = '/path/to/destination'
    file_types_to_move = ['.jpg', '.png']

    # 调用任务
    organize_folder_structure.delay(target_folder, destination_folder, file_types_to_move)