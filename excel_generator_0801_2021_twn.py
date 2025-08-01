# 代码生成时间: 2025-08-01 20:21:07
import os
from celery import Celery
from openpyxl import Workbook

"""
Excel表格自动生成器
这个程序使用Celery和openpyxl库来生成Excel表格
"""

# 配置Celery
app = Celery('excel_generator',
             broker='pyamqp://guest@localhost//')  # 使用RabbitMQ作为消息代理

# 定义任务函数
@app.task
def generate_excel(data, filename):
    """
    生成Excel表格的任务函数

    :param data: 要写入Excel的数据
    :type data: list
    :param filename: Excel文件的名称
    :type filename: str
    """
    try:
        # 创建一个Excel工作簿
        wb = Workbook()
        ws = wb.active
        ws.title = 'Sheet1'

        # 将数据写入Excel
        for row_data in data:
            ws.append(row_data)

        # 保存Excel文件
        wb.save(filename=filename)
        print(f"Excel文件已生成: {filename}")
    except Exception as e:
        # 错误处理
        print(f"生成Excel文件时发生错误: {e}")

# 示例用法
if __name__ == '__main__':
    data = [['Name', 'Age'], ['Alice', 25], ['Bob', 30]]  # 示例数据
    generate_excel.delay(data, 'example.xlsx')  # 异步生成Excel文件
