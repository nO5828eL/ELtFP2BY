# 代码生成时间: 2025-08-06 16:35:32
import os
import zipfile
from celery import Celery

# 配置Celery
app = Celery(
    'unzip_tool',
    broker='pyamqp://guest@localhost//',
    backend='rpc://'
)

@app.task(name='unzip_tool.unzip_file')
def unzip_file(file_path, destination):
    '''
    解压文件到指定目录。
    :param file_path: 压缩文件的路径。
    :param destination: 目标解压目录。
    :return: 解压结果。
    '''
    try:
        # 检查文件是否存在
        if not os.path.exists(file_path):
            raise FileNotFoundError(f'文件 {file_path} 不存在。')

        # 检查目的地目录是否存在，不存在则创建
        if not os.path.exists(destination):
            os.makedirs(destination)

        # 解压文件
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(destination)

        return {
            'status': 'success',
            'message': f'文件 {file_path} 已成功解压到 {destination}。'
        }
    except zipfile.BadZipFile:
        return {'status': 'error', 'message': '文件不是有效的zip文件。'}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}

if __name__ == '__main__':
    # 测试解压工具
    file_path = 'path/to/your/zip/file.zip'
    destination = 'path/to/your/destination/directory'
    result = unzip_file(file_path, destination)
    print(result)