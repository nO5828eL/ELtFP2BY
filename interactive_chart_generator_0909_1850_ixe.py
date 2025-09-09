# 代码生成时间: 2025-09-09 18:50:38
# interactive_chart_generator.py

"""
An interactive chart generator using Python and Celery framework.
"""

import os
from celery import Celery
from flask import Flask, request, jsonify
from flask_cors import CORS
from plotly.offline import plot
import pandas as pd
import json

# Initialize Flask application
app = Flask(__name__)
CORS(app)

# Initialize Celery
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

# Define a task to generate interactive chart
@celery.task
def generate_chart(chart_data, chart_type):
    """Generate an interactive chart using Plotly."""
    try:
        # Convert input data to DataFrame
        df = pd.DataFrame(chart_data)
        
        # Generate chart based on chart type
        if chart_type == 'line':
            fig = df.iplot(kind='line', asFigure=True)
        elif chart_type == 'bar':
            fig = df.iplot(kind='bar', asFigure=True)
        elif chart_type == 'scatter':
            fig = df.iplot(kind='scatter', asFigure=True)
        else:
            raise ValueError("Unsupported chart type")
        
        # Save chart as HTML file
        output_file = 'chart.html'
        plot(fig, filename=output_file, auto_open=False)
        return output_file
    except Exception as e:
        # Handle errors and return error message
        return str(e)

# Define a route to receive chart generation request
@app.route('/generate_chart', methods=['POST'])
def generate_chart_request():
    """Handle chart generation request."""
    try:
        # Get chart data and type from request
        request_data = request.get_json()
        chart_data = request_data['chart_data']
        chart_type = request_data['chart_type']
        
        # Call Celery task to generate chart
        output_file = generate_chart.delay(chart_data, chart_type).get()
        
        # Return chart file path
        return jsonify({'chart_file': output_file}), 200
    except Exception as e:
        # Handle errors and return error message
        return jsonify({'error': str(e)}), 400

# Define a route to serve generated chart files
@app.route('/chart/<filename>', methods=['GET'])
def serve_chart(filename):
    """Serve generated chart files."""
    try:
        # Check if chart file exists
        chart_file_path = os.path.join('charts', filename)
        if not os.path.exists(chart_file_path):
            return jsonify({'error': 'Chart file not found'}), 404
        
        # Serve chart file
        return app.send_static_file(chart_file_path)
    except Exception as e:
        # Handle errors and return error message
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Create 'charts' directory if not exists
    if not os.path.exists('charts'):
        os.makedirs('charts')
    
    # Start Flask application
    app.run(debug=True)