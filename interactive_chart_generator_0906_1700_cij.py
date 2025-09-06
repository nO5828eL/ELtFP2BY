# 代码生成时间: 2025-09-06 17:00:09
import os
import csv
from celery import Celery
from celery import shared_task
from flask import Flask, render_template, request, jsonify
import pandas as pd
import plotly.graph_objects as go
from plotly.offline import plot

# 配置Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')
app = Celery('tasks', broker='pyamqp://guest@localhost//')
app.conf.broker_url = 'pyamqp://guest@localhost//'
app.conf.result_backend = 'rpc://'
app.autodiscover_tasks(lambda: None)

# Flask应用配置
flask_app = Flask(__name__)

# 定义生成图表的任务
@shared_task
def generate_chart(data):
    # 将字符串数据转换为DataFrame
    df = pd.DataFrame(eval(data))
    # 创建图表
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['x'], y=df['y']))
    # 保存图表
    chart_html = plot(fig, output_type='div', show_link=False, include_plotlyjs=False)
    return chart_html

# Flask路由：接收数据并调用Celery任务
@flask_app.route('/generate_chart', methods=['POST'])
def receive_data():
    data = request.form.get('data')
    if not data:
        return jsonify({'error': 'No data provided'})
    try:
        # 调用Celery任务
        chart = generate_chart.delay(data).get()
        return jsonify({'chart': chart}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Flask路由：用于显示图表的页面
@flask_app.route('/')
def index():
    return render_template('index.html')

# 如果这是主模块，则运行Flask应用
if __name__ == '__main__':
    flask_app.run(debug=True)
