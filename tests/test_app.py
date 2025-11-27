from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_admin_list_members():
    response = client.get("/admin/members")
    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, list)
    assert body and body[0]["name"] == "张三"


def test_member_coupon_transfer():
    payload = {"coupon_id": "coupon-001", "to_member_phone": "13999990000"}
    response = client.post("/member/coupons/transfer", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body["coupon"]["status"] == "transferred"
    assert body["record"]["to_member_phone"] == "13999990000"


def test_merchant_redeem_and_report():
    login = client.post("/merchant/login", json={"phone": "13800001111", "password": "pass123"})
    assert login.status_code == 200

    redeem_payload = {"code": "coupon-002", "scene": "中餐厅"}
    redeem_response = client.post("/merchant/redemptions", json=redeem_payload)
    assert redeem_response.status_code == 200

    report_response = client.get("/admin/reports/redemptions")
    assert report_response.status_code == 200
    data = report_response.json()
    assert data["total"] >= 1


def test_admin_member_filters_and_basic_data():
    resp = client.get("/admin/members", params={"level": "GOLD"})
    assert resp.status_code == 200
    assert resp.json()[0]["level"] == "GOLD"

    scenes = client.get("/admin/basic/scenes")
    assert scenes.status_code == 200
    assert "中餐厅" in scenes.json()

    sales = client.get("/admin/basic/sales-reps")
    assert sales.status_code == 200
    assert isinstance(sales.json(), list)


def test_issue_products_and_reports():
    card_resp = client.post(
        "/admin/members/member-001/cards/issue", json={"template_id": "card-template-2888", "sales_rep": "Alice"}
    )
    assert card_resp.status_code == 200
    assert card_resp.json()["card"]["level"] == "DIAMOND"

    coupon_resp = client.post(
        "/admin/members/member-001/coupons/issue",
        json={"template_id": "coupon-template-breakfast", "quantity": 2},
    )
    assert coupon_resp.status_code == 200
    assert coupon_resp.json()["count"] == 2

    remaining = client.get("/admin/reports/remaining-products")
    assert remaining.status_code == 200
    assert remaining.json()["total"] >= 3


def test_modify_and_cancel_coupon_reports():
    modify = client.post(
        "/admin/coupons/modify-validity",
        json={"coupon_id": "coupon-002", "new_valid_to": "2000-01-01", "operator": "admin"},
    )
    assert modify.status_code == 200

    cancel = client.post(
        "/admin/coupons/cancel", json={"coupon_id": "coupon-001", "operator": "admin", "reason": "测试注销"}
    )
    assert cancel.status_code == 200

    mods = client.get("/admin/reports/modifications")
    assert mods.status_code == 200
    assert mods.json()["total"] >= 1

    cancels = client.get("/admin/reports/cancellations")
    assert cancels.status_code == 200
    assert cancels.json()["total"] >= 1

    expired = client.get("/admin/reports/expired-products")
    assert expired.status_code == 200
    assert expired.json()["total"] >= 1


def test_preview_endpoints_split():
    admin_preview = client.get("/preview/admin")
    merchant_preview = client.get("/preview/merchant")
    member_preview = client.get("/preview/member")
    merged_preview = client.get("/preview")

    assert admin_preview.status_code == 200
    assert merchant_preview.status_code == 200
    assert member_preview.status_code == 200
    assert merged_preview.status_code == 200
    assert admin_preview.json()["audience"] == "管理后台"
    assert merchant_preview.json()["audience"] == "商户核销端"
    assert member_preview.json()["audience"] == "会员端"
    merged = merged_preview.json()
    assert merged["admin"]["audience"] == "管理后台"
    assert merged["merchant"]["audience"] == "商户核销端"
    assert merged["member"]["audience"] == "会员端"
