# 代码生成时间: 2025-09-16 06:19:27
import os
import requests
from flask import Flask, request, jsonify
from celery import Celery
from celery.result import AsyncResult

# 创建Flask应用
app = Flask(__name__)

# 配置Celery
def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=os.environ.get('CELERY_RESULT_BACKEND',
                           'redis://localhost:6379/0'),
        broker=os.environ.get('CELERY_BROKER_URL',
                          'redis://localhost:6379/0'),
    )
    celery.conf.update(app.config)
    return celery

celery = make_celery(app)

# 定义异步任务
@celery.task(name='http.request_handler')
def async_http_request(url):
    """异步处理HTTP请求"""
    try:
        response = requests.get(url)
        response.raise_for_status()  # 检查请求是否成功
        return response.text
    except requests.RequestException as e:
        return f"Error: {e}"

# HTTP请求处理器路由
@app.route('/handle_request', methods=['POST'])
def handle_request():
    """处理HTTP请求并异步执行"""
    url = request.json.get('url')
    if not url:
        return jsonify({'error': 'URL is required'}), 400

    task = async_http_request.delay(url)
    return jsonify({'task_id': task.id}), 202

# 检查任务状态的路由
@app.route('/status/<task_id>')
def task_status(task_id):
    """检查任务状态并返回结果"""
    task = AsyncResult(task_id, app=celery)
    if task.state == 'PENDING':
        response = {"state": task.state, "status": "Pending..."}
    elif task.state != 'FAILURE':
        response = {"state": task.state, "result": task.get(timeout=10)}
    else:
        response = {"state": task.state, "status": str(task.info)}
    return jsonify(response)

if __name__ == '__main__':
    # 启动Flask应用
    app.run(debug=True)