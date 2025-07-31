# 代码生成时间: 2025-07-31 12:22:23
import os
import zipfile
import tarfile
from celery import Celery

# 配置Celery
app = Celery('file_uncompress_tool', broker='pyamqp://guest@localhost//')

# 压缩文件解压任务
@app.task
def uncompress_file(file_path, output_dir):
    """
    解压压缩文件到指定目录。
    
    Args:
        file_path (str): 压缩文件的路径。
        output_dir (str): 解压后的文件存放目录。
    
    Returns:
        bool: 解压操作是否成功。
    
    Raises:
        ValueError: 如果文件路径或输出目录无效。
    """
    if not os.path.exists(file_path):
        raise ValueError(f'File {file_path} does not exist.')
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    try:
        # 检测文件类型并解压
        if file_path.endswith('.zip'):
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(output_dir)
        elif file_path.endswith(('.tar', '.tar.gz', '.tar.bz2')):
            with tarfile.open(file_path, 'r') as tar_ref:
                tar_ref.extractall(output_dir)
        else:
            raise ValueError('Unsupported file format.')
        
        return True  # 解压成功
    except zipfile.BadZipFile:
        raise ValueError('Invalid zip file.')
    except tarfile.TarError:
        raise ValueError('Invalid tar file.')
    except Exception as e:
        raise e

# 程序入口点
if __name__ == '__main__':
    # 配置Celery
    app.conf.update(
        result_backend='rpc://',
        task_serializer='json',
        accept_content=['json'],
        timezone='UTC',
        enable_utc=True,
    )
    app.start()
    
    # 测试解压任务
    try:
        result = uncompress_file.delay('path/to/your/compressed/file.zip', 'path/to/output/directory')
        print(f'Uncompression result: {result.get()}')
    except Exception as e:
        print(f'An error occurred: {e}')