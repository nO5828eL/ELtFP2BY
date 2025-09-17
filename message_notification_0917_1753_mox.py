# 代码生成时间: 2025-09-17 17:53:15
from celery import Celery
from celery.exceptions import SoftTimeLimitExceeded
import logging
import sys

# 配置Celery
app = Celery('message_notification',
             broker='pyamqp://guest@localhost//',
             backend='rpc://')

# 配置日志记录器
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)

@app.task(soft_time_limit=10)  # 任务超时时间设置为10秒
def send_notification(message, recipient):
    """发送消息通知任务。

    参数:
    - message: 要发送的消息内容
    - recipient: 消息接收者

    返回:
    - 发送结果
    """
    try:
        logger.info(f'Sending notification to {recipient}')
        # 这里模拟发送消息的过程
        # 真实的实现中，可以使用邮件服务、短信服务等
        # 例如: send_email(message, recipient)
        # 这里只是打印信息来代替实际的发送过程
        print(f'Notification sent to {recipient}: {message}')
        return True
    except SoftTimeLimitExceeded:
        logger.error('Notification sending timed out')
        return False
    except Exception as e:
        logger.error(f'An error occurred: {e}')
        return False

if __name__ == '__main__':
    # 测试发送通知
    result = send_notification.delay('Hello, this is a test notification!', 'test@example.com')
    result.get()  # 阻塞等待任务完成并获取结果