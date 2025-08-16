"""针对 Flask 网页接口的基本测试。"""
import os
import sys

# 确保可以导入仓库根目录下的模块
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import webapp


def test_add_and_low_stock_via_http():
    client = webapp.app.test_client()
    # 清空库存以避免测试间相互影响
    webapp.manager.items.clear()

    res = client.post("/add", json={"name": "牛奶", "qty": 1})
    data = res.get_json()
    assert data["message"].startswith("[成功]")
    assert data["quantity"] == 1

    # 低库存查询应包含该商品
    res = client.get("/low-stock")
    data = res.get_json()
    assert any(item["name"] == "牛奶" for item in data)
