# 代码生成时间: 2025-09-21 23:18:18
import os
from flask import Flask, jsonify, request
from celery import Celery

# 初始化Flask应用
app = Flask(__name__)

# Celery配置
# TODO: 优化性能
def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=os.environ.get('CELERY_RESULT_BACKEND'),
        broker=os.environ.get('CELERY_BROKER_URL')
    )
    celery.conf.update(app.config)
    TaskBase = celery.Task
# 扩展功能模块

    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask  # 重写Task
    return celery

# 创建Celery实例
celery = make_celery(app)

# 定义一个Celery任务
@celery.task
def add(x, y):
# 扩展功能模块
    """异步任务：计算两个数的和"""
    return x + y
# TODO: 优化性能

# RESTful API接口
@app.route('/add', methods=['POST'])
def add_numbers():
    "