# 代码生成时间: 2025-09-24 12:15:19
import json
from celery import Celery
from celery.result import AsyncResult
from celery.exceptions import Ignore

# 配置Celery
app = Celery('form_validator', broker='pyamqp://guest@localhost//')

# 表单数据验证函数
def validate_form_data(data):
    # 检查数据是否包含必要的字段
    required_fields = ['name', 'email', 'age']
    for field in required_fields:
        if field not in data or not data[field]:
            raise ValueError(f"Missing or empty field: {field}")

    # 验证电子邮件地址格式
    if 'email' in data and not validate_email(data['email']):
        raise ValueError("Invalid email format")

    # 验证年龄是否在有效范围内
    if 'age' in data and (data['age'] < 0 or data['age'] > 120):
        raise ValueError("Age must be between 0 and 120")

    return True

# 电子邮件验证函数
def validate_email(email):
    import re
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email) is not None

# Celery任务函数
@app.task(bind=True)
def form_validator_task(self, data):
    try:
        # 异步执行表单数据验证
        result = validate_form_data(data)
        return json.dumps({'status': 'success', 'message': 'Form data is valid'})
    except ValueError as e:
        # 处理验证错误
        return json.dumps({'status': 'error', 'message': str(e)})
    except Exception as e:
        # 处理其他异常
        return json.dumps({'status': 'error', 'message': 'An unexpected error occurred'})

# 测试函数
def test_form_validator():
    # 测试数据
    data = {
        'name': 'John Doe',
        'email': 'john.doe@example.com',
        'age': 30
    }
    # 执行Celery任务
    result = form_validator_task.delay(data)
    # 获取任务结果
    while not result.ready():
        pass
    print(result.get())

if __name__ == '__main__':
    test_form_validator()