# 代码生成时间: 2025-08-23 02:32:46
import os
import logging
from celery import Celery
from celery import shared_task
from django.conf import settings
from django.core.management import call_command

# 配置Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')
app = Celery('database_migration_tool')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


# 设置日志记录器
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# 定义数据库迁移的Celery任务
@shared_task(bind=True)
def database_migration(self, **kwargs):
    """
    数据库迁移任务。
    
    参数:
    - self: Celery任务实例
    - **kwargs: 额外的参数
    
    返回:
    - None
    
    异常:
    - Exception: 如果迁移过程中发生错误
    """
    try:
        # 执行数据库迁移命令
        call_command('migrate')
        logger.info('Database migration completed successfully.')
    except Exception as e:
        logger.error('Database migration failed: %s', e)
        raise


# 以下是任务的使用示例
# 如果你想要手动触发迁移任务，可以使用以下代码
# database_migration.delay()

# 如果你想要定期执行迁移任务，可以将其添加到Celery的周期性任务中
# app.conf.beat_schedule = {
#     'database_migration_every_day': {
#         'task': 'database_migration_tool.database_migration',
#         'schedule': crontab(minute=0, hour=0),
#     },
# }
