"""简单的命令行界面，用于演示库存管理系统。

所有提示均采用文字和符号，避免依赖声音。
"""
from inventory import InventoryManager

def main() -> None:
    manager = InventoryManager()
    menu = (
        "\n请选择操作:\n"
        "1. 商品入库\n"
        "2. 商品出库\n"
        "3. 查看库存\n"
        "4. 查看低库存商品\n"
        "0. 退出\n"
    )
    while True:
        choice = input(menu + "> ")
        if choice == "1":
            name = input("商品名称: ")
            qty = int(input("数量: "))
            print(manager.add_item(name, qty))
        elif choice == "2":
            name = input("商品名称: ")
            qty = int(input("数量: "))
            print(manager.remove_item(name, qty))
        elif choice == "3":
            name = input("商品名称: ")
            print(f"{name} 当前库存: {manager.get_quantity(name)}")
        elif choice == "4":
            lows = manager.low_stock_items()
            if not lows:
                print("[提示] 所有商品库存充足")
            else:
                for item in lows:
                    print(f"[警告] {item.name} 库存仅剩 {item.quantity}")
        elif choice == "0":
            print("再见！")
            break
        else:
            print("[错误] 无效的选择")

if __name__ == "__main__":
    main()
