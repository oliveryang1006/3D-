"""基础库存管理逻辑。

该模块以纯文本提示为主，便于听障用户理解。
"""
from dataclasses import dataclass
from typing import Dict, List

@dataclass
class Item:
    """表示一种商品。"""
    name: str
    quantity: int = 0

class InventoryManager:
    """简单的内存库存管理。"""

    def __init__(self, low_stock_threshold: int = 5) -> None:
        self.items: Dict[str, Item] = {}
        self.low_stock_threshold = low_stock_threshold

    def add_item(self, name: str, qty: int = 1) -> str:
        """入库商品。

        返回适合视觉展示的提示文本。
        """
        item = self.items.get(name)
        if item:
            item.quantity += qty
        else:
            self.items[name] = Item(name=name, quantity=qty)
        return f"[成功] 已入库 {name} x{qty}"

    def remove_item(self, name: str, qty: int = 1) -> str:
        """出库商品。

        若库存不足，返回带有错误提示的文本。
        """
        item = self.items.get(name)
        if not item or item.quantity < qty:
            return f"[错误] {name} 库存不足"
        item.quantity -= qty
        return f"[成功] 已出库 {name} x{qty}"

    def get_quantity(self, name: str) -> int:
        """查询某商品库存"""
        item = self.items.get(name)
        return item.quantity if item else 0

    def low_stock_items(self) -> List[Item]:
        """返回低库存商品列表。"""
        return [i for i in self.items.values() if i.quantity <= self.low_stock_threshold]
