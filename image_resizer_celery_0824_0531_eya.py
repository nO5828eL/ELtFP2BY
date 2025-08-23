# 代码生成时间: 2025-08-24 05:31:05
import os
from PIL import Image
from celery import Celery
from celery.utils.log import get_task_logger

# 配置Celery
app = Celery('tasks',
             broker='pyamqp://guest@localhost//',
             backend='rpc://')

# 获取日志记录器
logger = get_task_logger(__name__)


@app.task(bind=True)
def resize_image(self, image_path, output_path, new_width, new_height):
    """
    调整图片尺寸的任务

    :param image_path: 原始图片路径
    :param output_path: 输出图片路径
    :param new_width: 新的图片宽度
    :param new_height: 新的图片高度
    :return: True if resize success, False otherwise
    """
    try:
        with Image.open(image_path) as img:
            # 调整图片尺寸
            img = img.resize((new_width, new_height), Image.ANTIALIAS)
            # 保存调整后的图片
            img.save(output_path)
            logger.info(f'Image resized successfully: {image_path} -> {output_path}')
            return True
    except IOError as e:
        logger.error(f'Failed to resize image {image_path}: {e}')
        return False


def resize_images_in_directory(directory, output_directory, new_width, new_height):
    """
    遍历目录中的所有图片并批量调整尺寸

    :param directory: 图片存储目录
    :param output_directory: 输出图片存储目录
    :param new_width: 新的图片宽度
    :param new_height: 新的图片高度
    """
    for filename in os.listdir(directory):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            image_path = os.path.join(directory, filename)
            output_path = os.path.join(output_directory, filename)
            # 发送任务到Celery
            resize_image.delay(image_path, output_path, new_width, new_height)
    logger.info(f'All images in {directory} are being resized...')


def main():
    # 使用配置实例化Celery
    app.conf.update(app_name='ImageResizer')

    # 图片目录和输出目录
    image_directory = 'path/to/image_directory'
    output_directory = 'path/to/output_directory'

    # 新的图片尺寸
    new_width = 800
    new_height = 600

    # 确保输出目录存在
    os.makedirs(output_directory, exist_ok=True)

    # 启动图片尺寸调整任务
    resize_images_in_directory(image_directory, output_directory, new_width, new_height)

if __name__ == '__main__':
    main()