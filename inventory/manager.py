"""基础库存管理逻辑。

该模块以纯文本提示为主，便于听障用户理解。
"""
from dataclasses import dataclass
from typing import Dict, List

@dataclass
class Item:
    """表示一种商品及其入库信息。"""

    name: str
    spec: str
    quantity: int = 0
    production_date: str = ""
    expiry_date: str = ""
    supplier: str = ""
    purchase_date: str = ""
    invoice_number: str = ""

class InventoryManager:
    """简单的内存库存管理。"""

    def __init__(self, low_stock_threshold: int = 5) -> None:
        self.items: Dict[str, Item] = {}
        self.low_stock_threshold = low_stock_threshold

    def add_item(
        self,
        name: str,
        spec: str,
        qty: int,
        production_date: str,
        expiry_date: str,
        supplier: str,
        purchase_date: str,
        invoice_number: str,
    ) -> str:
        """入库商品，并记录必要信息。

        返回适合视觉展示的提示文本。
        """
        item = self.items.get(name)
        if item:
            item.quantity += qty
            item.spec = spec
            item.production_date = production_date
            item.expiry_date = expiry_date
            item.supplier = supplier
            item.purchase_date = purchase_date
            item.invoice_number = invoice_number
        else:
            self.items[name] = Item(
                name=name,
                spec=spec,
                quantity=qty,
                production_date=production_date,
                expiry_date=expiry_date,
                supplier=supplier,
                purchase_date=purchase_date,
                invoice_number=invoice_number,
            )
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
