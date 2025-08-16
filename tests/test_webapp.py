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

    res = client.post(
        "/add",
        json={
            "name": "牛奶",
            "spec": "1L",
            "qty": 1,
            "production_date": "2023-01-01",
            "expiry_date": "2023-06-01",
            "supplier": "供应商B",
            "purchase_date": "2023-03-01",
            "invoice_number": "INV-002",
        },
    )
    data = res.get_json()
    assert data["message"].startswith("[成功]")
    assert data["quantity"] == 1
    assert webapp.manager.items["牛奶"].spec == "1L"

    # 低库存查询应包含该商品
    res = client.get("/low-stock")
    data = res.get_json()
    assert any(item["name"] == "牛奶" for item in data)


def test_index_page_and_form_submission():
    client = webapp.app.test_client()
    webapp.manager.items.clear()

    res = client.post(
        "/add",
        data={
            "name": "糖浆",
            "spec": "500ml",
            "qty": "3",
            "production_date": "2023-02-01",
            "expiry_date": "2024-02-01",
            "supplier": "供应商C",
            "purchase_date": "2023-04-01",
            "invoice_number": "INV-003",
        },
        follow_redirects=True,
    )
    text = res.get_data(as_text=True)
    assert "[成功]" in text
    assert "糖浆" in text  # 低库存列表包含该商品
    assert webapp.manager.items["糖浆"].spec == "500ml"

    res = client.get("/")
    assert res.status_code == 200
    assert "低库存商品" in res.get_data(as_text=True)
