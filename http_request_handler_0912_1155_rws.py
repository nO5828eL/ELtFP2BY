# 代码生成时间: 2025-09-12 11:55:00
import requests
from celery import Celery
from flask import Flask, request, jsonify
import logging

# 配置Flask
app = Flask(__name__)

# 配置Celery
app.config['CELERY_BROKER_URL'] = 'amqp://guest:guest@localhost//'  # 使用RabbitMQ作为消息代理
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'  # 使用Redis作为结果后端

# 初始化Celery
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

# 定义一个异步任务函数，用于处理HTTP请求
@celery.task
def handle_http_request(url, method, data=None):
    """
    异步处理HTTP请求
    :param url: 请求的URL
    :param method: 请求的方法，例如'GET', 'POST'
    :param data: 发送的数据，仅在POST请求中使用
    :return: HTTP响应内容
    """
    try:
        response = requests.request(method, url, data=data)
        response.raise_for_status()  # 检查请求是否成功
# 添加错误处理
        return response.text
    except requests.exceptions.RequestException as e:
# 增强安全性
        logging.error(f'HTTP请求失败: {e}')
        return None

# 定义Flask路由，接收HTTP请求并分发任务
@app.route('/send_request', methods=['POST'])
def send_request():
    try:
        # 从请求中获取参数
        url = request.json['url']
        method = request.json['method'].upper()
        data = request.json.get('data')

        # 调用异步任务
        result = handle_http_request.delay(url, method, data)

        # 返回任务ID供查询结果
        return jsonify({'task_id': result.id}), 202
    except KeyError as e:
        return jsonify({'error': f'缺少参数: {e}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)