# 代码生成时间: 2025-08-16 03:23:22
from celery import Celery
from datetime import datetime
import random

# 配置Celery
app = Celery('data_generator', broker='pyamqp://guest@localhost//')


# 数据生成器任务
@app.task
def generate_data(seed):
    """
    生成测试数据并返回，种子用于确保结果的可重复性。
    """
    try:
        # 模拟数据生成逻辑
        data = {
            'timestamp': datetime.now().isoformat(),
            'random_number': random.randint(1, 100),
            'seed': seed
        }
        # 这里可以添加更多的数据生成逻辑
        return data
    except Exception as e:
        # 错误处理
        raise ValueError(f'Data generation failed with seed {seed}: {e}')


if __name__ == '__main__':
    # 测试生成数据的任务
    seed = 42  # 可以改变这个种子来生成不同的测试数据
    result = generate_data.delay(seed)
    print(f'Generated data with seed {seed}:
{result.get(timeout=10)}')
