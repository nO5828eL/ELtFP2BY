# 代码生成时间: 2025-09-10 00:39:05
import celery
def create_celery_app():
    # Create a new Celery application
    app = celery.Celery('tasks',
                      broker='pyamqp://guest@localhost//',
                      backend='rpc://')
    return app

def add(app):
    # Define a task that adds two numbers
    def add_task(x, y):
        return x + y
    app.add_task(add_task)

def hello(app):
    # Define a task that prints 'Hello World'
    def hello_task():
        print('Hello World')
    app.add_task(hello_task)

def schedule_jobs(app):
    # Schedule periodic execution of tasks
    app.conf.beat_schedule = {
        'add-every-30-seconds': {
            'task': 'tasks.add',
            'schedule': 30.0,  # seconds
            'args': (16, 16)
        },
        'hello-every-minute': {
            'task': 'tasks.hello',
            'schedule': 60.0,  # seconds
        },
    }

if __name__ == '__main__':
    app = create_celery_app()
    add(app)
    hello(app)
    schedule_jobs(app)
    app.start()
