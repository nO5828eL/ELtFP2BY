# 代码生成时间: 2025-08-23 21:30:39
import json
from celery import Celery, Task

"""
API响应格式化工具
使用CELERY框架实现异步处理
"""

# 配置CELERY
app = Celery('api_response_formatter', broker='pyamqp://guest@localhost//')


class ApiResponseFormatterTask(Task):
    """
    CELERY任务类，用于格式化API响应
    """
    def run(self, response_data, status_code):
        """
        执行API响应格式化任务
        :param response_data: 原始响应数据
        :param status_code: HTTP状态码
        :return: 格式化后的响应数据
        """
        try:
            # 尝试将原始响应数据转换为JSON格式
            response_data = json.dumps(response_data, ensure_ascii=False)
            # 格式化响应数据
            formatted_response = {
                'status_code': status_code,
                'data': response_data
            }
            return formatted_response
        except Exception as e:
            # 处理异常情况
            return {'error': str(e)}


# 示例用法
if __name__ == '__main__':
    # 创建CELERY任务实例
    task = ApiResponseFormatterTask()
    # 执行任务
    result = task.delay({'key': 'value'}, 200)
    # 获取任务结果
    print(result.get())
