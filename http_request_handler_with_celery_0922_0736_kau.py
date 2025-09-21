# 代码生成时间: 2025-09-22 07:36:41
import os
import requests
from flask import Flask, request
from celery import Celery

# 定义Flask应用
app = Flask(__name__)

# 配置Celery
app.config['CELERY_BROKER_URL'] = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379/0')
app.config['CELERY_RESULT_BACKEND'] = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')

# 初始化Celery实例
celery_app = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery_app.conf.update(app.config)

# 定义一个Celery任务，用于处理HTTP请求
@celery_app.task
def process_request(url, method='GET', **kwargs):
    """
    处理HTTP请求的任务。
    参数:
    url (str): 请求的URL。
    method (str): 请求方法，默认为'GET'。
    **kwargs: 其他关键字参数，用于传递请求头、数据等。
    返回:
    response (requests.Response): HTTP请求的响应对象。
    """
    try:
        if method.upper() == 'GET':
            response = requests.get(url, **kwargs)
        elif method.upper() == 'POST':
            response = requests.post(url, **kwargs)
        # 可以根据需要添加更多请求方法的处理
        return response
    except requests.RequestException as e:
        # 处理请求异常
        return {'error': str(e)}

# 定义Flask路由，接收HTTP请求并触发Celery任务
@app.route('/send_request', methods=['POST'])
def send_request():
    """
    接收HTTP请求并触发Celery任务的路由。
    参数:
    无
    返回:
    json_response (dict): 包含任务结果的JSON响应。
    """
    data = request.json  # 从请求中获取JSON数据
    url = data.get('url')
    method = data.get('method', 'GET')
    kwargs = data.get('kwargs', {})

    # 触发Celery任务
    task = process_request.delay(url, method, **kwargs)
    return {'task_id': task.id}, 202

# 启动Flask应用
if __name__ == '__main__':
    app.run(debug=True)