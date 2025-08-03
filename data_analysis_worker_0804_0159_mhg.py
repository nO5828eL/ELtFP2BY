# 代码生成时间: 2025-08-04 01:59:34
import os
import json
from celery import Celery
from celery import shared_task

# 配置Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')
app = Celery('data_analysis_worker')
app.config_from_object('django_celery_beat')
app.autodiscover_tasks(lambda: None)


# 数据统计分析器任务
@shared_task
def data_analysis_task(data):
    """
    统计数据分析器任务
    
    参数:
    data (dict): 包含待分析数据的字典
    
    返回:
    dict: 包含分析结果的字典
    
    异常:
    ValueError: 如果输入数据不合法
    """
    try:
        # 检查数据是否为空
        if not data:
            raise ValueError("输入数据为空")
        
        # 这里可以添加具体的数据分析逻辑
        # 例如，计算数据的平均值、中位数等
        # 为了演示，这里仅返回输入数据
        result = {"status": "success", "data": data}
        
        return result
    
    except Exception as e:
        # 处理异常情况
        return {"status": "error", "message": str(e)}


# 以下是扩展任务的示例
@shared_task
def data_analysis_task_v2(data):
    """
    统计数据分析器任务（扩展）
    
    参数:
    data (dict): 包含待分析数据的字典
    
    返回:
    dict: 包含分析结果的字典
    
    异常:
    ValueError: 如果输入数据不合法
    """
    try:
        # 检查数据是否为空
        if not data:
            raise ValueError("输入数据为空")
        
        # 这里可以添加更复杂的数据分析逻辑
        # 例如，计算数据的标准差、方差等
        # 为了演示，这里仅返回输入数据
        result = {"status": "success", "data": data, "extended_info": "Extended analysis results"}
        
        return result
    
    except Exception as e:
        # 处理异常情况
        return {"status": "error", "message": str(e)}


# 以下是如何使用任务的示例
if __name__ == "__main__":
    # 示例数据
    sample_data = {"values": [1, 2, 3, 4, 5]}
    
    # 调用任务
    result = data_analysis_task.delay(sample_data)
    
    # 获取结果
    result = result.get()
    
    print(json.dumps(result, indent=4))
