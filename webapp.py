"""基于 Flask 的简单网页和 API 接口，提供库存管理功能。

网页端以清晰的文字和颜色提示操作结果；同时保留 JSON 接口，便于编程访问。
"""
from flask import Flask, request, jsonify, render_template, redirect, url_for
from inventory import InventoryManager

app = Flask(__name__)
manager = InventoryManager()


@app.route("/")
def index() -> str:
    """显示带有表单的主页。"""
    message = request.args.get("msg")
    items = manager.low_stock_items()
    return render_template("index.html", message=message, items=items)


@app.route("/add", methods=["POST"])
def add_item():
    """入库商品。"""
    data = request.get_json(silent=True) or request.form
    name = data.get("name")
    qty = int(data.get("qty", 1))
    message = manager.add_item(name, qty)
    if request.is_json:
        return jsonify({"message": message, "quantity": manager.get_quantity(name)})
    return redirect(url_for("index", msg=message))


@app.route("/remove", methods=["POST"])
def remove_item():
    """出库商品。"""
    data = request.get_json(silent=True) or request.form
    name = data.get("name")
    qty = int(data.get("qty", 1))
    message = manager.remove_item(name, qty)
    if request.is_json:
        return jsonify({"message": message, "quantity": manager.get_quantity(name)})
    return redirect(url_for("index", msg=message))


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
