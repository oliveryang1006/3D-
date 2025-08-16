"""基于 Flask 的简单网页接口，提供库存管理功能。

所有提示均以 JSON 形式返回，便于视觉化呈现。
"""
from flask import Flask, request, jsonify
from inventory import InventoryManager

app = Flask(__name__)
manager = InventoryManager()


@app.route("/")
def index() -> str:
    """主页说明。"""
    return (
        "<h1>咖啡厅库存管理</h1>"
        "<p>使用 POST /add 或 /remove 进行入库和出库，"
        "GET /low-stock 查看低库存商品。</p>"
    )


@app.route("/add", methods=["POST"])
def add_item():
    """入库商品。"""
    data = request.get_json(silent=True) or request.form
    name = data.get("name")
    qty = int(data.get("qty", 1))
    message = manager.add_item(name, qty)
    return jsonify({"message": message, "quantity": manager.get_quantity(name)})


@app.route("/remove", methods=["POST"])
def remove_item():
    """出库商品。"""
    data = request.get_json(silent=True) or request.form
    name = data.get("name")
    qty = int(data.get("qty", 1))
    message = manager.remove_item(name, qty)
    return jsonify({"message": message, "quantity": manager.get_quantity(name)})


@app.route("/low-stock")
def low_stock():
    """返回低库存商品。"""
    items = [
        {"name": item.name, "quantity": item.quantity}
        for item in manager.low_stock_items()
    ]
    return jsonify(items)


if __name__ == "__main__":
    app.run(debug=True)
