# 代码生成时间: 2025-08-30 12:53:19
import os
from celery import Celery
from flask import Flask, request, jsonify
from plotly.offline import plot
from plotly.graph_objs import Bar
from celery.signals import worker_process_init
import pandas as pd

# 配置Celery
app = Celery('tasks', broker='pyamqp://guest@localhost//')
app.conf.broker_url = 'pyamqp://guest@localhost//'
app.conf.result_backend = 'rpc://'

# 启动Flask应用
flask_app = Flask(__name__)

# 定义Celery任务
@app.task
def generate_chart(data):
    # 异常处理
    try:
        # 将数据转换为DataFrame
        df = pd.DataFrame(data)
        # 创建图表
        fig = plot(
            Bar(
                x=df['Category'],
                y=df['Value']
            ),
            filename=f'chart_{os.urandom(16).hex()}.html',
            auto_open=False
        )
        # 返回图表文件路径
        return {'path': fig}
    except Exception as e:
        # 错误处理
        return {'error': str(e)}

# 定义Flask路由
@flask_app.route('/chart', methods=['POST'])
def chart_route():
    # 获取数据
    data = request.get_json()
    # 调用Celery任务
    task = generate_chart.delay(data)
    # 返回任务ID
    return jsonify({'task_id': task.id}), 202

# 在Flask应用中注册Celery任务结果回调
@flask_app.route('/chart/<task_id>/result', methods=['GET'])
def get_chart_result(task_id):
    # 检查任务状态
    task = app.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {
            'state': task.state,
            'status': 'Pending...'
        }
    elif task.state == 'FAILURE':
        response = {
            'state': task.state,
            'status': str(task.info)
        }
    else:
        response = {
            'state': task.state,
            'status': 'Completed',
            'path': task.result
        }
    return jsonify(response)

# 启动Flask应用
if __name__ == '__main__':
    flask_app.run(debug=True)