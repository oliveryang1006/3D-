from datetime import date

from fastapi import APIRouter, HTTPException

from ..schemas import Member, TransferRequest, UpdateMemberRequest
from ..storage import store

router = APIRouter(prefix="/member", tags=["member"])


def _current_member() -> Member:
    member = store.get_member("member-001")
    if not member:
        raise HTTPException(status_code=404, detail="会员不存在")
    return member


@router.get("/profile", response_model=Member)
def get_profile():
    return _current_member()


@router.post("/login/wechat", response_model=Member)
def wechat_login():
    """模拟公众号手机号授权后的快捷登录。"""
    return _current_member()


@router.patch("/profile", response_model=Member)
def update_profile(request: UpdateMemberRequest):
    member = _current_member()
    if request.name:
        member.name = request.name
    return member


@router.get("/cards")
def my_cards():
    member = _current_member()
    return member.cards


@router.get("/coupons")
def my_coupons(status: str | None = None):
    member = _current_member()
    today = date.today()
    for coupon in member.coupons:
        if coupon.valid_to < today and coupon.status == "active":
            coupon.status = "expired"
    if status:
        return [c for c in member.coupons if c.status == status]
    return member.coupons


@router.get("/coupons/{coupon_id}")
def coupon_detail(coupon_id: str):
    member = _current_member()
    coupon = next((c for c in member.coupons if c.id == coupon_id), None)
    if not coupon:
        raise HTTPException(status_code=404, detail="卡券不存在")
    return {
        "coupon": coupon,
        "qr": f"QR-{coupon.id}",
        "code": coupon.id,
        "usage": f"请在{coupon.scene or '指定'}场景出示二维码核销",
    }


@router.post("/coupons/transfer")
def transfer_coupon(request: TransferRequest):
    member = _current_member()
    coupon = next((c for c in member.coupons if c.id == request.coupon_id), None)
    if not coupon:
        raise HTTPException(status_code=404, detail="卡券不存在")
    if not coupon.transferrable:
        raise HTTPException(status_code=400, detail="该卡券不可转赠")
    if coupon.status != "active":
        raise HTTPException(status_code=400, detail="仅可转赠未使用的卡券")
    if coupon.valid_to < date.today():
        coupon.status = "expired"
        raise HTTPException(status_code=400, detail="券码已过期")
    coupon.status = "transferred"
    transfer_record = store.record_transfer(member_id=member.id, coupon_id=coupon.id, to_member_phone=request.to_member_phone)
    return {"message": "已生成转赠记录", "to": request.to_member_phone, "coupon": coupon, "record": transfer_record}
