from fastapi import APIRouter, HTTPException

from ..schemas import LoginRequest, RedemptionRecord, RedemptionRequest
from ..storage import store

router = APIRouter(prefix="/merchant", tags=["merchant"])


@router.post("/login")
def login(request: LoginRequest):
    verifier = store.find_verifier(request.phone, request.password)
    if not verifier:
        raise HTTPException(status_code=401, detail="账号或密码错误")
    return {"operator_id": verifier["operator_id"], "scene": verifier["scene"]}


@router.post("/redemptions", response_model=RedemptionRecord)
def redeem(request: RedemptionRequest, operator: str = "verifier-001"):
    """模拟核销员在指定场景核销券码。"""
    result = store.find_coupon_by_code(request.code)
    if not result:
        raise HTTPException(status_code=404, detail="未找到券码对应的会员或卡券")
    member, coupon = result
    if coupon.status == "used":
        raise HTTPException(status_code=400, detail="券码已被核销")
    if coupon.status == "transferred":
        raise HTTPException(status_code=400, detail="券码已转赠，等待接收人使用")
    if coupon.status == "expired":
        raise HTTPException(status_code=400, detail="券码已过期")
    record = store.record_redemption(member_id=member.id, coupon_id=coupon.id, scene=request.scene, operator=operator)
    coupon.status = "used"
    return record


@router.get("/redemptions", response_model=list[RedemptionRecord])
def my_redemptions(operator: str = "verifier-001"):
    """核销员查看自己的核销记录。"""
    data = [r for r in store.redemptions if r.operator == operator]
    return data
