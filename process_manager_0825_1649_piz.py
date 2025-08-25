# 代码生成时间: 2025-08-25 16:49:55
import os
import time
from celery import Celery

# 定义Celery应用，使用Redis作为消息代理
app = Celery('process_manager', broker='pyamqp://guest@localhost//')

class ProcessManager:
    def __init__(self):
        # 初始化进程管理器
        self.tasks = {}

    def start_process(self, task_name, task_func, *args, **kwargs):
        """
        启动一个新的进程，执行指定的任务
        :param task_name: 任务的名称
        :param task_func: 要执行的任务函数
        :param args: 任务函数的位置参数
        :param kwargs: 任务函数的关键字参数
        :return: None
        """
        try:
            self.tasks[task_name] = app.send_task(task_func, args=args, kwargs=kwargs)
            print(f"Task {task_name} started with task_id: {self.tasks[task_name].id}")
        except Exception as e:
            print(f"Error starting task {task_name}: {e}")

    def stop_process(self, task_name):
        """
        停止一个正在运行的进程
        :param task_name: 任务的名称
        :return: None
        """
        if task_name in self.tasks:
            task = self.tasks[task_name]
            if task.status == 'FAILURE':
                print(f"Task {task_name} has failed and cannot be stopped")
                return
            elif task.status == 'SUCCESS':
                print(f"Task {task_name} has finished and cannot be stopped")
                return
            else:
                print(f"Stopping task {task_name} with task_id: {self.tasks[task_name].id}")
                self.tasks[task_name].retry(countdown=0, max_retries=0)  # 尝试立即重试任务，实际上会终止它
        else:
            print(f"Task {task_name} not found")

# 示例任务函数
@app.task
def sample_task(name):
    """
    一个简单的示例任务，打印一条消息并暂停一段时间
    :param name: 要打印的名字
    """
    print(f"Hello, {name}!")
    time.sleep(10)

if __name__ == '__main__':
    manager = ProcessManager()
    # 启动任务
    manager.start_process('sample_task', sample_task, 'World')
    try:
        # 模拟长时间运行，让任务有机会执行
        while True:
            for task_name, task in manager.tasks.items():
                status = task.status
                print(f"Task {task_name} has status: {status}")
            if os.path.exists('stop'):  # 检测到文件'stop'时停止程序
                break
            time.sleep(5)
    except KeyboardInterrupt:
        print('Stopping all tasks...')
        for task_name in manager.tasks:
            manager.stop_process(task_name)
    finally:
        # 清理任务
        for task_name in manager.tasks:
            task = manager.tasks[task_name]
            if task.status == 'PENDING':
                task.retry(countdown=0, max_retries=0)
        print('All tasks stopped or finished.')