# 代码生成时间: 2025-09-05 01:17:20
import os
import time
from celery import Celery

# 配置Celery
app = Celery('performance_test',
             broker='amqp://guest@localhost//',
             backend='rpc://')

# 性能测试任务
@app.task(bind=True)
def performance_task(self, num_iterations=1000):
    """
    性能测试任务，执行指定次数的耗时操作。
    :param self: Celery任务实例
    :param num_iterations: 迭代次数，默认为1000次
    """
    start_time = time.time()
    for _ in range(num_iterations):
        # 模拟耗时操作
        time.sleep(0.001)
    end_time = time.time()
    elapsed_time = end_time - start_time
    total_time = elapsed_time / num_iterations
    print(f'Iteration Time: {total_time:.6f} seconds, Total Time: {elapsed_time:.6f} seconds')
    return {'iterations': num_iterations, 'total_time': elapsed_time, 'avg_time': total_time}

# 性能测试脚本入口
def main():
    """
    性能测试脚本的主函数。
    """
    if 'CIRCLECI' in os.environ:
        # 如果是CI环境，设置更高的迭代次数
        num_iterations = 10000
    else:
        num_iterations = 1000
    
    # 调用性能测试任务
    result = performance_task.delay(num_iterations)
    result.get()

if __name__ == '__main__':
    main()