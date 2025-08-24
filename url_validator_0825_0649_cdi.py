# 代码生成时间: 2025-08-25 06:49:22
from celery import Celery
from urllib.parse import urlparse
import requests
from requests.exceptions import RequestException
from celery.signals import worker_process_init
from requests.exceptions import ConnectionError, Timeout

# 初始化Celery应用
app = Celery('url_validator', broker='pyamqp://guest:guest@localhost//')

# 配置Celery任务
@app.task(bind=True)
def validate_url(self, url):
    """
    验证URL链接的有效性。
    
    :param self: Celery任务实例
    :param url: 需要验证的URL字符串
    :return: 一个字典，包含URL验证结果
    """
    try:
        # 解析URL
        parsed_url = urlparse(url)
        # 检查URL是否包含必要组件
        if not all([parsed_url.scheme, parsed_url.netloc]):
            return {"valid": False, "message": "Invalid URL format"}

        # 发起HEAD请求检查URL是否可达
        response = requests.head(url, timeout=5)
        # 根据响应状态码判断URL是否有效
        if response.status_code == 200:
            return {"valid": True, "message": "URL is valid"}
        else:
            return {"valid": False, "message": "URL is not reachable, status code: {}".format(response.status_code)}
    except (ConnectionError, Timeout) as e:
        return {"valid": False, "message": "Failed to reach URL: {}".format(e)}
    except RequestException as e:
        return {"valid": False, "message": "Request exception: {}".format(e)}
    except Exception as e:
        return {"valid": False, "message": "An unexpected error occurred: {}".format(e)}

# 配置Celery工作进程初始化信号，用于设置日志记录或其他初始化任务
@worker_process_init.connect()
def configure_logging(sender=None, **kwargs):
    from celery import current_worker
    current_worker.logger.info("Worker process initialized")
    # 可以在这里设置日志记录器等

# 以下是如何使用该任务的示例
if __name__ == '__main__':
    # 这里可以添加代码来启动Celery worker或者调用任务
    pass