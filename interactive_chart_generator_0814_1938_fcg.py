# 代码生成时间: 2025-08-14 19:38:27
# interactive_chart_generator.py

"""
Interactive Chart Generator using Python and Celery framework.
This program is designed to generate interactive charts based on user input.
"""

import json
from celery import Celery
from flask import Flask, request, jsonify
from flask_celery import Celery
from plotly.offline import plot
import pandas as pd
import os

app = Flask(__name__)

# Celery configuration
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

# Initialize Celery
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

# Celery task for generating interactive charts
@celery.task
def generate_chart(data):
    """
    Generate an interactive chart based on the provided data.
    :param data: A dictionary containing chart configuration and data.
    :return: A JSON string of the chart image.
    """
    try:
        # Create a Pandas DataFrame from the data
        df = pd.DataFrame(data['data'])
        
        # Generate the chart
        fig = plot(df, filename='chart.html', output_type='file', 
                  include_plotlyjs=True, auto_open=False)
        
        # Save the chart to a temporary file
        with open('chart.html', 'r') as file:
            chart_image = file.read()
        
        # Remove the temporary file
        os.remove('chart.html')
        
        # Return the chart image as a JSON string
        return json.dumps(chart_image)
    except Exception as e:
        # Handle any errors that occur during chart generation
        return json.dumps({'error': str(e)})

# Flask route for submitting chart generation requests
@app.route('/generate_chart', methods=['POST'])
def submit_chart_request():
    """
   接收用户提交的图表生成请求，并将其排队到Celery。
    """
    try:
        # Get the chart data from the request
        chart_data = request.get_json()
        
        # Validate the chart data
        if not isinstance(chart_data, dict) or 'data' not in chart_data:
            return jsonify({'error': 'Invalid chart data'}), 400
        
        # Queue the chart generation task to Celery
        task = generate_chart.delay(chart_data)
        
        # Return the task ID and a success message
        return jsonify({'task_id': task.id, 'message': 'Chart generation task queued'}), 200
    except Exception as e:
        # Handle any errors that occur during request processing
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)