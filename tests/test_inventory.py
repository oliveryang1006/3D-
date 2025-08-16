"""针对库存管理的基本单元测试。"""
import os
import sys
import pytest

# 确保可以导入仓库根目录下的模块
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from inventory import InventoryManager

def test_add_and_query():
    manager = InventoryManager()
    manager.add_item("咖啡豆", 10)
    assert manager.get_quantity("咖啡豆") == 10


def test_remove_and_low_stock():
    manager = InventoryManager(low_stock_threshold=2)
    manager.add_item("牛奶", 3)
    manager.remove_item("牛奶", 2)
    assert manager.get_quantity("牛奶") == 1
    lows = manager.low_stock_items()
    assert len(lows) == 1 and lows[0].name == "牛奶"
