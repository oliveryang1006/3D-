from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class MembershipCard(BaseModel):
    id: str
    name: str
    level: str
    price: int
    valid_from: date
    valid_to: date
    benefits: List[str] = Field(default_factory=list)
    status: str = "active"


class Coupon(BaseModel):
    id: str
    name: str
    type: str
    value: float
    threshold: Optional[float] = None
    valid_from: date
    valid_to: date
    transferrable: bool = False
    status: str = "active"
    scene: Optional[str] = None


class ConsumptionRecord(BaseModel):
    id: str
    amount: float
    description: str
    occurred_at: datetime


class Member(BaseModel):
    id: str
    name: str
    phone: str
    level: str
    registered_at: datetime
    sales_rep: Optional[str] = None
    cards: List[MembershipCard] = Field(default_factory=list)
    coupons: List[Coupon] = Field(default_factory=list)
    redemption_history: List["RedemptionRecord"] = Field(default_factory=list)
    transfer_history: List["TransferRecord"] = Field(default_factory=list)
    consumption_history: List[ConsumptionRecord] = Field(default_factory=list)


class RedemptionRequest(BaseModel):
    code: str = Field(..., description="券码或二维码解析值")
    scene: str = Field(..., description="核销场景，如中餐厅")


class RedemptionRecord(BaseModel):
    id: str
    member_id: str
    coupon_id: str
    scene: str
    operator: str
    redeemed_at: datetime


class TransferRecord(BaseModel):
    id: str
    coupon_id: str
    from_member_id: str
    to_member_phone: str
    transferred_at: datetime


class TransferRequest(BaseModel):
    coupon_id: str
    to_member_phone: str


class UpdateMemberRequest(BaseModel):
    name: Optional[str] = None


class FreezeCardRequest(BaseModel):
    card_id: str
    reason: Optional[str] = None


class AdminReportFilters(BaseModel):
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    scene: Optional[str] = None
    operator: Optional[str] = None
    coupon_type: Optional[str] = None


class CardTemplate(BaseModel):
    id: str
    name: str
    level: str
    price: int
    valid_days: int
    benefits: List[str] = Field(default_factory=list)
    total: int = 0
    issued_count: int = 0


class CouponTemplate(BaseModel):
    id: str
    name: str
    type: str
    value: float
    threshold: Optional[float] = None
    valid_days: int
    transferrable: bool = False
    total: int = 0
    issued_count: int = 0
    scene: Optional[str] = None


class IssueCardRequest(BaseModel):
    template_id: str
    sales_rep: Optional[str] = None


class IssueCouponRequest(BaseModel):
    template_id: str
    quantity: int = 1


class ModifyValidityRequest(BaseModel):
    coupon_id: str
    new_valid_to: date
    operator: str


class ValidityModificationLog(BaseModel):
    id: str
    coupon_id: str
    operator: str
    before_valid_to: date
    after_valid_to: date
    modified_at: datetime


class CancelCouponRequest(BaseModel):
    coupon_id: str
    reason: Optional[str] = None
    operator: str


class CancellationLog(BaseModel):
    id: str
    coupon_id: str
    operator: str
    reason: Optional[str] = None
    cancelled_at: datetime


class RemainingProduct(BaseModel):
    product_id: str
    name: str
    type: str
    remaining: int


class LoginRequest(BaseModel):
    phone: str
    password: str


# 解决前向引用
Member.model_rebuild()
