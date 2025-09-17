# 代码生成时间: 2025-09-18 07:58:04
import os
from celery import Celery
from PIL import Image
from io import BytesIO

# 配置Celery
app = Celery('tasks', broker='pyamqp://guest@localhost//')
app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)

# 图片尺寸调整任务
@app.task
def resize_image(file_path, output_path, new_size):
    """
    调整图片尺寸的任务。
    
    参数:
    - file_path: 要调整尺寸的图片文件路径。
    - output_path: 调整尺寸后图片的保存路径。
    - new_size: 图片新尺寸的元组（width, height）。
    
    返回:
    - 调整尺寸后图片的保存路径。
    """
    try:
        # 打开图片文件
        with Image.open(file_path) as img:
            # 调整图片尺寸
            img = img.resize(new_size)
            # 保存调整后的图片
            img.save(output_path)
            return output_path
    except IOError as e:
        # 处理图片打开或保存时的错误
        print(f"Error resizing image {file_path}: {e}")
        return None

# 示例用法
if __name__ == '__main__':
    # 定义图片文件路径和输出路径
    input_images = ['image1.jpg', 'image2.jpg']
    output_images = ['resized_image1.jpg', 'resized_image2.jpg']
    new_size = (800, 600)  # 新尺寸

    # 对每张图片调用resize_image任务
    for input_image, output_image in zip(input_images, output_images):
        result = resize_image.delay(input_image, output_image, new_size)
        if result:
            print(f"Image resized and saved to {result}")
        else:
            print(f"Failed to resize image {input_image}")
