# 代码生成时间: 2025-09-12 22:22:34
import os
from celery import Celery

# 定义配置文件路径
CONFIG_FILE_PATH = 'config.json'

# 初始化Celery应用
app = Celery('config_manager',
             broker='pyamqp://guest@localhost//')
app.conf.update(
    result_backend='rpc://',
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    timezone='UTC',
    enable_utc=True)


# 读取配置文件
def load_config():
    """
    读取配置文件并返回配置字典。
    """
    try:
        with open(CONFIG_FILE_PATH, 'r') as f:
            config = f.read()
            return eval(config)
    except FileNotFoundError:
        raise FileNotFoundError(f'配置文件{CONFIG_FILE_PATH}未找到。')
    except Exception as e:
        raise Exception(f'读取配置文件时发生错误：{e}')


# 保存配置文件
def save_config(config):
    """
    将配置字典保存到配置文件中。
    """
    try:
        with open(CONFIG_FILE_PATH, 'w') as f:
            f.write(str(config))
    except Exception as e:
        raise Exception(f'保存配置文件时发生错误：{e}')


# Celery任务：读取配置
@app.task
def read_config_task():
    """
    Celery任务：读取配置文件并返回配置字典。
    """
    try:
        config = load_config()
        return config
    except Exception as e:
        return f'读取配置时发生错误：{e}'


# Celery任务：保存配置
@app.task
def save_config_task(config):
    """
    Celery任务：将配置字典保存到配置文件中。
    """
    try:
        save_config(config)
        return '配置保存成功'
    except Exception as e:
        return f'保存配置时发生错误：{e}'