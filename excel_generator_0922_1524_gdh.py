# 代码生成时间: 2025-09-22 15:24:17
import os
import pandas as pd
from celery import Celery

# 定义 Celery 应用
app = Celery('excel_generator', broker='pyamqp://guest@localhost//')

@app.task
def generate_excel(data, filename):
    """
    生成 Excel 文件的任务
    
    参数:
    data (list of dicts): 包含数据的列表，每个字典代表一行数据
    filename (str): 生成的 Excel 文件名
    
    返回:
    str: 文件路径
    """
    try:
        # 将数据转换为 DataFrame
        df = pd.DataFrame(data)
        # 确保文件名后缀为 .xlsx
        if not filename.endswith('.xlsx'):
            filename += '.xlsx'
        # 指定文件路径
        file_path = os.path.join('output', filename)
        # 保存为 Excel 文件
        df.to_excel(file_path, index=False)
        return file_path
    except Exception as e:
        # 错误处理
        raise Exception(f'生成 Excel 文件失败: {str(e)}')

# 以下代码用于测试，实际使用时应通过 Celery 控制台或其他调度器调用任务
if __name__ == '__main__':
    # 测试数据
    test_data = [
        {'Name': 'Alice', 'Age': 25},
        {'Name': 'Bob', 'Age': 30}
    ]
    # 测试文件名
    test_filename = 'test_excel'
    # 调用任务
    result = generate_excel.delay(test_data, test_filename)
    # 打印结果
    print(f'Excel 文件已生成: {result.get()}