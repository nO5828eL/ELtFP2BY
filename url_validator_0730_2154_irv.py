# 代码生成时间: 2025-07-30 21:54:19
import requests
from celery import Celery
from urllib.parse import urlparse
from datetime import timedelta
from celery.schedules import crontab

# 配置Celery
app = Celery('url_validator',
             broker='amqp://guest:guest@localhost//',
             backend='rpc://')

# 配置周期性任务
app.conf.beat_schedule = {
    'validate-urls-every-5-minutes': {
        'task': 'url_validator.tasks.validate_urls',
        'schedule': timedelta(minutes=5)
    }
}

@app.task
def validate_url(url):
    """验证单个URL链接的有效性"""
    try:
        # 解析URL
        result = urlparse(url)
        if all([result.scheme, result.netloc]):
            # 发起HEAD请求检查URL是否可达
            response = requests.head(url, allow_redirects=True, timeout=5)
            if response.status_code == 200:
                return f"{url} is valid"
            else:
                return f"{url} is invalid with status code {response.status_code}"
        else:
            return f"{url} is not a valid URL"
    except requests.ConnectionError:
        return f"{url} connection error"
    except requests.Timeout:
        return f"{url} timeout error"
    except Exception as e:
        return f"{url} encountered an error: {str(e)}"

@app.task
def validate_urls(urls):
    """批量验证URL链接的有效性"""
    results = {}
    for url in urls:
        results[url] = validate_url.delay(url)
    return results
