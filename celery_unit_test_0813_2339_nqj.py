# 代码生成时间: 2025-08-13 23:39:28
import unittest
from unittest.mock import patch, MagicMock
from celery import Celery
from your_module import tasks  # 假设tasks是你定义的包含Celery任务的模块


class TestCeleryTasks(unittest.TestCase):
    """测试Celery任务的单元测试类"""

    def setUp(self):
        """设置测试环境"""
        self.app = Celery('your_module', broker='pyamqp://guest@localhost//', backend='rpc://')
        self.app.conf.update(CELERY_ALWAYS_EAGER=True)  # 使任务同步执行，便于测试
        self.app.conf.update(CELERY_EAGER_PROPAGATES_EXCEPTIONS=True)  # 使异常能被抛出

    def test_task(self):
        """测试Celery任务是否正常执行"""
        with patch('your_module.tasks.some_task') as mock_task:
            mock_task.return_value = 'Expected result'
            result = tasks.some_task()  # 调用任务
            self.assertEqual(result, 'Expected result', '任务执行结果不正确')

            # 检查任务是否被调用
            mock_task.assert_called_once_with()

    def test_task_with_parameters(self):
        """测试带参数的Celery任务"""
        with patch('your_module.tasks.some_task_with_params') as mock_task:
            mock_task.return_value = 'Expected result with params'
            result = tasks.some_task_with_params('param1', 'param2')
            self.assertEqual(result, 'Expected result with params', '带参数的任务执行结果不正确')

            # 检查任务是否被调用
            mock_task.assert_called_once_with('param1', 'param2')

    def test_task_exception(self):
        """测试Celery任务在出错时的行为"""
        with patch('your_module.tasks.task_that_raises_exception') as mock_task:
            mock_task.side_effect = Exception('Expected exception')
            with self.assertRaises(Exception) as context:
                tasks.task_that_raises_exception()
            self.assertEqual(str(context.exception), 'Expected exception', '异常未按预期抛出')


if __name__ == '__main__':
    unittest.main()
