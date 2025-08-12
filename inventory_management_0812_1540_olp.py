# 代码生成时间: 2025-08-12 15:40:31
import os
import logging
from celery import Celery

# 配置Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')
app = Celery('inventory_management')
app.config_from_object('django.conf:settings', namespace='CELERY')

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 库存管理类
class InventoryManager:
    def __init__(self, inventory):
        self.inventory = inventory

    def add_item(self, item, quantity):
        """添加库存项
        Args:
            item (str): 库存项名称
            quantity (int): 数量
        """
        if item in self.inventory:
            self.inventory[item] += quantity
        else:
            self.inventory[item] = quantity
        logger.info(f"Added {quantity} {item}(s) to inventory.")

    def remove_item(self, item, quantity):
        """移除库存项
        Args:
            item (str): 库存项名称
            quantity (int): 数量
        Returns:
            bool: 是否成功移除
        """
        if item in self.inventory and self.inventory[item] >= quantity:
            self.inventory[item] -= quantity
            if self.inventory[item] == 0:
                del self.inventory[item]
            logger.info(f"Removed {quantity} {item}(s) from inventory.")
            return True
        else:
            logger.error(f"Failed to remove {quantity} {item}(s) from inventory. Insufficient quantity.")
            return False

    def check_inventory(self, item):
        """检查库存
        Args:
            item (str): 库存项名称
        Returns:
            int: 库存数量
        """
        return self.inventory.get(item, 0)

# Celery任务
@app.task
def add_item_task(item, quantity):
    """异步添加库存项任务"""
    inventory = {"item1": 10, "item2": 5}  # 示例库存
    manager = InventoryManager(inventory)
    manager.add_item(item, quantity)

@app.task
def remove_item_task(item, quantity):
    """异步移除库存项任务"""
    inventory = {"item1": 10, "item2": 5}  # 示例库存
    manager = InventoryManager(inventory)
    success = manager.remove_item(item, quantity)
    return success

if __name__ == '__main__':
    # 测试代码
    inventory = {"item1": 10, "item2": 5}
    manager = InventoryManager(inventory)
    print("Initial inventory:", inventory)
    manager.add_item("item1", 5)
    print("Inventory after adding item1:", manager.inventory)
    if manager.remove_item("item2", 3):
        print("Inventory after removing item2:", manager.inventory)
    else:
        print("Failed to remove item2.")
    print("Item1 quantity:", manager.check_inventory("item1"))
    print("Item3 quantity:", manager.check_inventory("item3"))
    
    # 异步任务测试
    result = remove_item_task.delay("item1", 2)
    print("Remove item1 task status:", result.status)
