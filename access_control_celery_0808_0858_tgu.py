# 代码生成时间: 2025-08-08 08:58:12
# access_control_celery.py
# A Python script that demonstrates access control using Celery

from celery import Celery
from functools import wraps
from flask import Flask, request, jsonify

# Initialize Flask application
app = Flask(__name__)

# Initialize Celery
app.config['CELERY_BROKER_URL'] = 'amqp://guest:guest@localhost//'
app.config['CELERY_RESULT_BACKEND'] = 'rpc://'
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

# Decorator for handling access control
def access_control(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if the user has the required token
        token = request.headers.get('Authorization')
        if not token or not verify_token(token):
            return jsonify({'error': 'Unauthorized access'}), 401
        return f(*args, **kwargs)
    return decorated_function

# Dummy function to verify token (should be replaced with actual verification logic)
def verify_token(token):
    # Placeholder for token verification logic
    # In a real-world scenario, this would check against a database or external service
    return True

# Define a Celery task for testing
@celery.task
def test_task():
    return 'Task executed successfully'

# Route for triggering the Celery task
@app.route('/trigger-task', methods=['POST'])
@access_control
def trigger_task():
    # Trigger the Celery task
    result = test_task.apply_async()
    return jsonify({'task_id': result.id}), 200

# Route for checking task status
@app.route('/check-task/<task_id>', methods=['GET'])
@access_control
def check_task(task_id):
    task = test_task.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {'state': task.state, 'status': 'Pending...'}
    elif task.state == 'FAILURE':
        response = {'state': task.state, 'status': str(task.info)}
    else:
        response = {'state': task.state, 'status': 'Task executed successfully'}
    return jsonify(response)

# Main function to run the application
if __name__ == '__main__':
    app.run(debug=True)
