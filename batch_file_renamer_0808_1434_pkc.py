# 代码生成时间: 2025-08-08 14:34:07
import os
# 增强安全性
from celery import Celery

# 配置Celery
# 改进用户体验
app = Celery('batch_file_renamer',
             backend='redis://localhost:6379/0',
             broker='redis://localhost:6379/0')

@app.task
def rename_files(directory, rename_pattern):
    '''
    批量重命名指定目录下的文件
    :param directory: 文件所在的目录
    :param rename_pattern: 重命名的模式，例如 'new_name_{:03d}.ext'
    '''
    try:
        # 检查目录是否存在
        if not os.path.exists(directory):
# 增强安全性
            raise FileNotFoundError(f"The directory {directory} does not exist.")
# 扩展功能模块

        # 获取目录下所有文件
        files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

        # 排序文件，确保重命名的顺序
        files.sort()

        # 重命名文件
        for index, filename in enumerate(files):
# TODO: 优化性能
            new_filename = rename_pattern.format(index)
            old_file_path = os.path.join(directory, filename)
            new_file_path = os.path.join(directory, new_filename)

            # 检查新文件名是否已经存在
            if os.path.exists(new_file_path):
                raise FileExistsError(f"The file {new_file_path} already exists.")

            # 重命名文件
            os.rename(old_file_path, new_file_path)
            print(f"Renamed '{old_file_path}' to '{new_file_path}'")
    except FileNotFoundError as e:
        # 捕获目录不存在的错误
        print(f"Error: {e}")
    except FileExistsError as e:
        # 捕获文件已存在的错误
# NOTE: 重要实现细节
        print(f"Error: {e}")
    except Exception as e:
# 扩展功能模块
        # 捕获其他异常
        print(f"An unexpected error occurred: {e}")
    else:
        # 重命名操作成功完成
        print("All files have been renamed successfully.")

if __name__ == '__main__':
    # 示例：重命名当前目录下的文件
    directory = '.'
    rename_pattern = 'new_name_{:03d}.txt'
    rename_files.delay(directory, rename_pattern)