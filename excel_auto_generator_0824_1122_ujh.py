# 代码生成时间: 2025-08-24 11:22:27
import csv
import os
from celery import Celery
from celery import shared_task
from openpyxl import Workbook

# 配置Celery
app = Celery('excel_auto_generator')
app.config_from_object('celeryconfig')


@shared_task
def generate_excel(data, filename):
    '''
    生成Excel文件的任务
    :param data: 要写入Excel的数据
    :param filename: Excel文件的名称
    :return: 无
    '''
    try:
        # 创建一个Excel工作簿
        workbook = Workbook()
        sheet = workbook.active
        sheet.title = 'Data'

        # 将数据写入Excel
        for row in data:
            sheet.append(row)

        # 保存Excel文件
        workbook.save(filename)
        print(f'Excel file {filename} generated successfully.')
    except Exception as e:
        # 错误处理
        print(f'Error generating Excel file: {e}')


# 以下是如何使用这个任务的例子
# 假设我们有一些数据要写入Excel
example_data = [
    ['Name', 'Age', 'City'],
    ['Alice', 24, 'New York'],
    ['Bob', 30, 'Los Angeles'],
    ['Charlie', 20, 'Chicago']
]

# 调用任务生成Excel文件
# generate_excel.delay(example_data, 'example.xlsx')

# 请注意，为了运行Celery任务，需要有一个运行中的Celery worker，
# 并且需要有'celeryconfig.py'文件来配置Celery。

# 这里的代码只是一个示例，实际部署时需要根据实际情况调整配置和代码逻辑。