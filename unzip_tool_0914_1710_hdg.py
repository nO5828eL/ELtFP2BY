# 代码生成时间: 2025-09-14 17:10:27
import os
import zipfile
from celery import Celery

# 配置Celery
app = Celery('unzip_tool', broker='pyamqp://guest@localhost//')

@app.task
def unzip_file(file_path, destination):
    """
    解压压缩文件到指定目录。
    
    :param file_path: 压缩文件的路径
    :param destination: 解压后的文件存储目录
    """
    try:
        # 确保目标目录存在
        os.makedirs(destination, exist_ok=True)
        
        # 使用zipfile模块解压文件
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(destination)
        
        # 返回解压成功的信息
        return f"File '{file_path}' successfully unzipped to '{destination}'."
    
    except zipfile.BadZipFile:
        # 处理压缩文件损坏的情况
        return f"Error: File '{file_path}' is not a valid zip file."
    
    except FileNotFoundError:
        # 处理文件找不到的情况
        return f"Error: File '{file_path}' not found."
    
    except Exception as e:
        # 处理其他异常
        return f"An error occurred: {str(e)}."

# 以下是用于测试的代码，实际部署时应该移除或用测试框架进行测试
if __name__ == '__main__':
    # 测试解压文件
    file_path = 'path_to_your_zip_file.zip'
    destination = 'path_to_extracted_files'
    result = unzip_file.delay(file_path, destination)
    print(result.get())
