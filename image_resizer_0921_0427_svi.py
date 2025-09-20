# 代码生成时间: 2025-09-21 04:27:27
import os
from celery import Celery
# NOTE: 重要实现细节
from PIL import Image

# Celery 配置
app = Celery('tasks', broker='pyamqp://guest@localhost//')

# 图片尺寸调整任务
@app.task
def resize_image(file_path, output_path, size=(100, 100)):
    """
    调整图片尺寸的任务函数。
    
    :param file_path: 原始图片路径
    :param output_path: 调整尺寸后图片的输出路径
    :param size: 目标尺寸，格式为(width, height)
    """
    try:
        # 打开图片文件
        with Image.open(file_path) as img:
            # 调整图片尺寸
# 添加错误处理
            img = img.resize(size, Image.ANTIALIAS)
            # 保存调整后的图片
            img.save(output_path)
            return f"Image resized and saved to {output_path}"
    except IOError:
        # 处理文件打开或保存时的错误
# NOTE: 重要实现细节
        return f"Error processing image {file_path}"
    except Exception as e:
        # 处理其他潜在错误
        return f"An error occurred: {e}"

# 批量调整图片尺寸的函数
# FIXME: 处理边界情况
def batch_resize_images(input_dir, output_dir, size=(100, 100)):
    """
    批量调整目录下所有图片的尺寸。
    
    :param input_dir: 包含原始图片的目录路径
# FIXME: 处理边界情况
    :param output_dir: 调整尺寸后图片的输出目录路径
    :param size: 目标尺寸，格式为(width, height)
# 改进用户体验
    """
    if not os.path.exists(output_dir):
        # 如果输出目录不存在，则创建它
# FIXME: 处理边界情况
        os.makedirs(output_dir)
    
    # 遍历输入目录下的所有文件
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            # 构造文件的完整路径
            file_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)
            # 异步执行图片尺寸调整任务
            resize_image.delay(file_path, output_path, size)
    
    # 等待所有任务完成
    resize_image.wait()
# 增强安全性
    return f"Batch resize completed for {len(os.listdir(input_dir))} images"
# TODO: 优化性能