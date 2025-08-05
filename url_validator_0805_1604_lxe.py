# 代码生成时间: 2025-08-05 16:04:06
from celery import Celery
import requests
from urllib.parse import urlparse
from typing import Any, Tuple

# 定义Celery应用
app = Celery('url_validator', broker='pyamqp://guest@localhost//')

# 定义URL验证任务
@app.task
def validate_url(url: str) -> Tuple[bool, str]:
    """
    验证给定的URL是否有效。
    
    参数:
    url (str): 需要验证的URL字符串。
    
    返回:
    Tuple[bool, str]: 一个元组，其中包含布尔值表示URL是否有效，
                     以及描述信息。
    """
    try:
        # 解析URL
        parsed_url = urlparse(url)
        if not all([parsed_url.scheme, parsed_url.netloc]):
            return False, "Invalid URL: Scheme and netloc are required."

        # 检查URL是否可以访问
        response = requests.head(url, allow_redirects=True, timeout=5)
        if response.status_code == 200:
            return True, "URL is valid and accessible."
        else:
            return False, f"URL is not accessible. Status code: {response.status_code}"
    except requests.RequestException as e:
        return False, f"URL validation failed: {str(e)}"
    except Exception as e:
        return False, f"An unexpected error occurred: {str(e)}"
