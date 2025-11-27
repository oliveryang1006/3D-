from datetime import date

from fastapi import APIRouter, HTTPException, Query

from ..schemas import (
    AdminReportFilters,
    CancelCouponRequest,
    FreezeCardRequest,
    IssueCardRequest,
    IssueCouponRequest,
    Member,
    ModifyValidityRequest,
    RedemptionRequest,
)
from ..storage import store

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/members", response_model=list[Member])
def list_members(
    name: str | None = Query(None),
    phone: str | None = Query(None),
    level: str | None = Query(None),
    registered_from: date | None = Query(None, description="注册起始日期"),
    registered_to: date | None = Query(None, description="注册结束日期"),
):
    """按姓名、手机号、等级、注册时间过滤会员列表。"""
    return store.list_members(
        name=name,
        phone=phone,
        level=level,
        registered_from=registered_from,
        registered_to=registered_to,
    )


@router.get("/members/{member_id}", response_model=Member)
def get_member(member_id: str):
    member = store.get_member(member_id)
    if not member:
        raise HTTPException(status_code=404, detail="会员不存在")
    return member


@router.post("/members/{member_id}/freeze")
def freeze_card(member_id: str, request: FreezeCardRequest):
    card = store.freeze_card(member_id=member_id, card_id=request.card_id, reason=request.reason)
    if not card:
        raise HTTPException(status_code=404, detail="会员或卡片不存在")
    return {"message": "已冻结", "card": card}


@router.post("/members/{member_id}/cards/issue")
def issue_card(member_id: str, request: IssueCardRequest):
    card = store.issue_card(member_id=member_id, template_id=request.template_id, sales_rep=request.sales_rep)
    if not card:
        raise HTTPException(status_code=404, detail="会员或卡模板不存在")
    return {"message": "已发放会员卡", "card": card}


@router.post("/members/{member_id}/coupons/issue")
def issue_coupons(member_id: str, request: IssueCouponRequest):
    coupons = store.issue_coupons(member_id=member_id, template_id=request.template_id, quantity=request.quantity)
    if not coupons:
        raise HTTPException(status_code=404, detail="会员或券模板不存在")
    return {"message": "已发放卡券", "count": len(coupons), "coupons": coupons}


@router.get("/reports/redemptions")
def redemption_report(
    start_date: date | None = Query(None, description="起始日期，格式YYYY-MM-DD"),
    end_date: date | None = Query(None, description="截止日期，格式YYYY-MM-DD"),
    scene: str | None = Query(None),
    operator: str | None = Query(None),
    coupon_type: str | None = Query(None),
):
    filters = AdminReportFilters(
        start_date=start_date,
        end_date=end_date,
        scene=scene,
        operator=operator,
        coupon_type=coupon_type,
    )
    data = store.list_redemptions(filters)
    return {"total": len(data), "items": data}


@router.get("/reports/transfers")
def transfer_report():
    logs = store.list_transfer_logs()
    return {"total": len(logs), "items": logs}


@router.get("/reports/remaining-products")
def remaining_products_report():
    items = store.list_remaining_products()
    return {"total": len(items), "items": items}


@router.get("/reports/expired-products")
def expired_products_report():
    items = store.list_expired_products()
    return {"total": len(items), "items": items}


@router.get("/reports/modifications")
def modification_logs_report():
    logs = store.list_modification_logs()
    return {"total": len(logs), "items": logs}


@router.get("/reports/cancellations")
def cancellations_report():
    logs = store.list_cancellation_logs()
    return {"total": len(logs), "items": logs}


@router.get("/basic/scenes")
def list_scenes():
    return store.list_scenes()


@router.get("/basic/sales-reps")
def list_sales_reps():
    return store.list_sales_reps()


@router.get("/products/card-templates")
def list_card_templates():
    return store.list_card_templates()


@router.get("/products/coupon-templates")
def list_coupon_templates():
    return store.list_coupon_templates()


@router.post("/redemptions")
def redeem_in_admin(request: RedemptionRequest, operator: str = "admin"):
    result = store.find_coupon_by_code(request.code)
    if not result:
        raise HTTPException(status_code=404, detail="未找到券码对应的会员或卡券")
    member, coupon = result
    if coupon.status in {"used", "cancelled"}:
        raise HTTPException(status_code=400, detail="券码不可用")
    if coupon.status == "transferred":
        raise HTTPException(status_code=400, detail="券码已转赠，等待接收人使用")
    if coupon.valid_to < date.today():
        coupon.status = "expired"
        raise HTTPException(status_code=400, detail="券码已过期")
    record = store.record_redemption(member_id=member.id, coupon_id=coupon.id, scene=request.scene, operator=operator)
    coupon.status = "used"
    return record


@router.post("/coupons/modify-validity")
def modify_validity(request: ModifyValidityRequest):
    log = store.modify_coupon_validity(request.coupon_id, request.new_valid_to, request.operator)
    if not log:
        raise HTTPException(status_code=404, detail="未找到卡券")
    return {"message": "有效期已调整", "log": log}


@router.post("/coupons/cancel")
def cancel_coupon(request: CancelCouponRequest):
    log = store.cancel_coupon(request.coupon_id, request.operator, request.reason)
    if not log:
        raise HTTPException(status_code=404, detail="未找到卡券")
    return {"message": "卡券已注销", "log": log}
