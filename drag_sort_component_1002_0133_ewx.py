# 代码生成时间: 2025-10-02 01:33:23
import celery
from celery import shared_task

# 定义Celery应用
app = celery.Celery('tasks', broker='pyamqp://guest@localhost//')

# 模拟数据列表
data_list = [1, 5, 3, 8, 6, 2, 4]


@shared_task
def sort_data(data):
    """
    异步排序数据列表。
    
    :param data: 需要排序的数据列表
    :return: 排序后的数据列表
    """
    try:
        sorted_data = sorted(data)
        return sorted_data
    except Exception as e:
        # 错误处理
        raise ValueError(f'Failed to sort data: {e}')


# 模拟前端拖拽排序后调用后端排序任务
def drag_sort_handler(new_order):
    """
    模拟前端调用后端排序任务。
    
    :param new_order: 前端拖拽排序后的顺序列表
    """
    # 调用Celery任务
    result = sort_data.delay(new_order)
    # 等待任务完成并获取结果
    sorted_list = result.get()
    return sorted_list

# 示例用法
def main():
    # 假设这是前端传回的新顺序列表
    new_order = [4, 2, 6, 1, 8, 3, 5]
    sorted_list = drag_sort_handler(new_order)
    print(f'Sorted list: {sorted_list}')

if __name__ == '__main__':
    main()