# 代码生成时间: 2025-09-07 05:02:10
import json\
from celery import Celery\
from celery.exceptions import SoftTimeLimitExceeded\
\
# 配置Celery\
app = Celery('api_response_formatter', broker='pyamqp://guest@localhost//')\
\
# API响应格式化工具类\
class ApiResponseFormatter:\
    def __init__(self, data):\
        """
        初始化API响应格式化工具
        :param data: 原始API响应数据
        """
        self.data = data\
\
    def format_response(self):\
        """
        格式化API响应数据
        :return: 格式化后的API响应数据
        """
        try:\
            # 尝试解析JSON数据\
            data = json.loads(self.data)\
        except ValueError as e:\
            # 如果数据不是有效的JSON格式，返回错误信息\
            return self._error_response("Invalid JSON format", str(e))\
\
        # 检查数据是否包含必要的键\
        required_keys = ["status", "message", "data"]\
        if not all(key in data for key in required_keys):\
            return self._error_response("Missing required keys", ", ".join(required_keys))\
\
        # 格式化响应数据\
        formatted_data = {\
            "status": data.get("status", "unknown"),\
            "message": data.get("message", "No message provided"),\
            "data": data.get("data", {})\
        }\
\
        return self._success_response(formatted_data)\
\
    def _success_response(self, data):\
        """
        创建成功的API响应\
        :param data: 响应数据\
        :return: 成功的API响应\
        """
        return {\
            "status": "success",\
            "message": "Request processed successfully",
            "data": data\
        }\
\
    def _error_response(self, message, details):\
        """
        创建错误的API响应\
        :param message: 错误消息\
        :param details: 错误详情\
        :return: 错误的API响应\
        """
        return {\
            "status": "error",
            "message": message,
            "details": details
        }\
\
# Celery任务，使用ApiResponseFormatter格式化API响应\
@app.task(soft_time_limit=10)\
def format_api_response(raw_data):\
    """
    Celery任务，用于格式化API响应\
    :param raw_data: 原始API响应数据\
    :return: 格式化后的API响应数据\
    """\
    try:\
        formatter = ApiResponseFormatter(raw_data)\
        return formatter.format_response()\
    except SoftTimeLimitExceeded:\
        return {"status": "error", "message": "Request timed out"}\
    except Exception as e:\
        return {"status": "error", "message": "An unexpected error occurred