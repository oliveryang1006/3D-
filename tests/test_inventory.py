"""针对库存管理的基本单元测试。"""
import os
import sys
import pytest

# 确保可以导入仓库根目录下的模块
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from inventory import InventoryManager

def test_add_and_query():
    manager = InventoryManager()
    manager.add_item(
        "咖啡豆",
        "250g",
        10,
        "2023-01-01",
        "2024-01-01",
        "供应商A",
        "2023-06-01",
        "INV-001",
    )
    item = manager.items["咖啡豆"]
    assert item.spec == "250g"
    assert manager.get_quantity("咖啡豆") == 10


def test_remove_and_low_stock():
    manager = InventoryManager(low_stock_threshold=2)
    manager.add_item(
        "牛奶",
        "1L",
        3,
        "2023-01-01",
        "2023-06-01",
        "供应商B",
        "2023-03-01",
        "INV-002",
    )
    manager.remove_item("牛奶", 2)
    assert manager.get_quantity("牛奶") == 1
    lows = manager.low_stock_items()
    assert len(lows) == 1 and lows[0].name == "牛奶"
