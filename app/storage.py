from __future__ import annotations

from datetime import date, datetime, timedelta
from typing import Dict, List, Optional

from .schemas import (
    AdminReportFilters,
    CancellationLog,
    CardTemplate,
    Coupon,
    CouponTemplate,
    Member,
    MembershipCard,
    RedemptionRecord,
    RemainingProduct,
    TransferRecord,
    ValidityModificationLog,
)


class InMemoryStore:
    def __init__(self) -> None:
        self.members: Dict[str, Member] = {}
        self.redemptions: List[RedemptionRecord] = []
        self.transfer_logs: List[TransferRecord] = []
        self.modification_logs: List[ValidityModificationLog] = []
        self.cancellation_logs: List[CancellationLog] = []
        self.scenes = ["中餐厅", "西餐厅", "前台", "康体中心"]
        self.sales_reps = ["Alice", "Bob", "Cathy"]
        self.card_templates: List[CardTemplate] = []
        self.coupon_templates: List[CouponTemplate] = []
        self.verifiers = {
            "13800001111": {"password": "pass123", "operator_id": "verifier-001", "scene": "前台"}
        }
        self._coupon_counter = 3
        self._seed()

    def _seed(self) -> None:
        today = date.today()
        self.card_templates = [
            CardTemplate(
                id="card-template-1988",
                name="金卡",
                level="GOLD",
                price=1988,
                valid_days=365,
                benefits=["9折房价", "康体中心8折"],
                total=50,
            ),
            CardTemplate(
                id="card-template-2688",
                name="白金卡",
                level="PLATINUM",
                price=2688,
                valid_days=365,
                benefits=["85折房价", "行政酒廊使用"],
                total=30,
            ),
            CardTemplate(
                id="card-template-2888",
                name="钻石卡",
                level="DIAMOND",
                price=2888,
                valid_days=365,
                benefits=["8折房价", "行政酒廊+SPA"],
                total=10,
            ),
        ]
        self.coupon_templates = [
            CouponTemplate(
                id="coupon-template-upgrade",
                name="房型升级券",
                type="升级券",
                value=1,
                valid_days=90,
                transferrable=True,
                total=120,
                scene="前台",
            ),
            CouponTemplate(
                id="coupon-template-cash",
                name="无门槛代金券",
                type="代金券",
                value=200,
                threshold=None,
                valid_days=60,
                total=200,
                scene="中餐厅",
            ),
            CouponTemplate(
                id="coupon-template-breakfast",
                name="早餐折扣券",
                type="折扣券",
                value=8.5,
                threshold=100,
                valid_days=30,
                total=100,
                scene="西餐厅",
            ),
        ]

        default_cards = [self._issue_card_from_template(self.card_templates[0], today)]
        coupons = [
            self._issue_coupon_from_template(self.coupon_templates[0], today),
            self._issue_coupon_from_template(self.coupon_templates[1], today),
        ]
        member = Member(
            id="member-001",
            name="张三",
            phone="13800000000",
            level="GOLD",
            registered_at=datetime.utcnow(),
            sales_rep=self.sales_reps[0],
            cards=default_cards,
            coupons=coupons,
            consumption_history=[],
        )
        self.members[member.id] = member

    def list_members(
        self,
        name: Optional[str] = None,
        phone: Optional[str] = None,
        level: Optional[str] = None,
        registered_from: Optional[date] = None,
        registered_to: Optional[date] = None,
    ) -> List[Member]:
        data = list(self.members.values())
        if name:
            data = [m for m in data if name in m.name]
        if phone:
            data = [m for m in data if phone in m.phone]
        if level:
            data = [m for m in data if m.level == level]
        if registered_from:
            data = [m for m in data if m.registered_at.date() >= registered_from]
        if registered_to:
            data = [m for m in data if m.registered_at.date() <= registered_to]
        return data

    def get_member(self, member_id: str) -> Optional[Member]:
        return self.members.get(member_id)

    def list_card_templates(self) -> List[CardTemplate]:
        return list(self.card_templates)

    def list_coupon_templates(self) -> List[CouponTemplate]:
        return list(self.coupon_templates)

    def _issue_card_from_template(self, template: CardTemplate, start_date: date) -> MembershipCard:
        template.issued_count += 1
        return MembershipCard(
            id=f"card-{template.id}-{template.issued_count}",
            name=template.name,
            level=template.level,
            price=template.price,
            valid_from=start_date,
            valid_to=start_date + timedelta(days=template.valid_days),
            benefits=template.benefits,
        )

    def _issue_coupon_from_template(self, template: CouponTemplate, start_date: date) -> Coupon:
        template.issued_count += 1
        self._coupon_counter += 1
        return Coupon(
            id=f"coupon-{self._coupon_counter:03d}",
            name=template.name,
            type=template.type,
            value=template.value,
            threshold=template.threshold,
            valid_from=start_date,
            valid_to=start_date + timedelta(days=template.valid_days),
            transferrable=template.transferrable,
            scene=template.scene,
        )

    def issue_card(self, member_id: str, template_id: str, sales_rep: Optional[str]) -> Optional[MembershipCard]:
        member = self.members.get(member_id)
        template = next((t for t in self.card_templates if t.id == template_id), None)
        if not member or not template:
            return None
        card = self._issue_card_from_template(template, date.today())
        member.cards.append(card)
        if sales_rep:
            member.sales_rep = sales_rep
        return card

    def issue_coupons(self, member_id: str, template_id: str, quantity: int) -> List[Coupon]:
        member = self.members.get(member_id)
        template = next((t for t in self.coupon_templates if t.id == template_id), None)
        if not member or not template:
            return []
        issued: List[Coupon] = []
        today = date.today()
        for _ in range(quantity):
            issued.append(self._issue_coupon_from_template(template, today))
        member.coupons.extend(issued)
        return issued

    def find_coupon_by_code(self, code: str) -> Optional[tuple[Member, Coupon]]:
        """扫描券码后查找所属会员和券对象。当前使用券 ID 作为券码。"""
        today = date.today()
        for member in self.members.values():
            for coupon in member.coupons:
                if coupon.id == code:
                    if coupon.valid_to < today:
                        coupon.status = "expired"
                    return member, coupon
        return None

    def freeze_card(self, member_id: str, card_id: str, reason: Optional[str]) -> Optional[MembershipCard]:
        member = self.members.get(member_id)
        if not member:
            return None
        for card in member.cards:
            if card.id == card_id:
                card.status = "frozen"
                if reason:
                    card.benefits.append(f"冻结原因: {reason}")
                return card
        return None

    def record_redemption(self, member_id: str, coupon_id: str, scene: str, operator: str) -> RedemptionRecord:
        record = RedemptionRecord(
            id=f"redemption-{len(self.redemptions)+1}",
            member_id=member_id,
            coupon_id=coupon_id,
            scene=scene,
            operator=operator,
            redeemed_at=datetime.utcnow(),
        )
        self.redemptions.append(record)
        member = self.members.get(member_id)
        if member:
            member.redemption_history.append(record)
        return record

    def record_transfer(self, member_id: str, coupon_id: str, to_member_phone: str) -> TransferRecord:
        record = TransferRecord(
            id=f"transfer-{len(self.transfer_logs)+1}",
            coupon_id=coupon_id,
            from_member_id=member_id,
            to_member_phone=to_member_phone,
            transferred_at=datetime.utcnow(),
        )
        self.transfer_logs.append(record)
        member = self.members.get(member_id)
        if member:
            member.transfer_history.append(record)
        return record

    def modify_coupon_validity(self, coupon_id: str, new_valid_to: date, operator: str) -> Optional[ValidityModificationLog]:
        for member in self.members.values():
            for coupon in member.coupons:
                if coupon.id == coupon_id:
                    log = ValidityModificationLog(
                        id=f"modify-{len(self.modification_logs)+1}",
                        coupon_id=coupon_id,
                        operator=operator,
                        before_valid_to=coupon.valid_to,
                        after_valid_to=new_valid_to,
                        modified_at=datetime.utcnow(),
                    )
                    coupon.valid_to = new_valid_to
                    if new_valid_to < date.today():
                        coupon.status = "expired"
                    self.modification_logs.append(log)
                    return log
        return None

    def cancel_coupon(self, coupon_id: str, operator: str, reason: Optional[str]) -> Optional[CancellationLog]:
        for member in self.members.values():
            for coupon in member.coupons:
                if coupon.id == coupon_id:
                    coupon.status = "cancelled"
                    log = CancellationLog(
                        id=f"cancel-{len(self.cancellation_logs)+1}",
                        coupon_id=coupon_id,
                        operator=operator,
                        reason=reason,
                        cancelled_at=datetime.utcnow(),
                    )
                    self.cancellation_logs.append(log)
                    return log
        return None

    def list_redemptions(self, filters: Optional[AdminReportFilters] = None) -> List[RedemptionRecord]:
        data = list(self.redemptions)
        if not filters:
            return data
        if filters.scene:
            data = [r for r in data if r.scene == filters.scene]
        if filters.operator:
            data = [r for r in data if r.operator == filters.operator]
        if filters.coupon_type:
            data = [r for r in data if r.coupon_id.startswith(filters.coupon_type)]
        if filters.start_date:
            data = [r for r in data if r.redeemed_at.date() >= filters.start_date]
        if filters.end_date:
            data = [r for r in data if r.redeemed_at.date() <= filters.end_date]
        return data

    def list_transfer_logs(self) -> List[TransferRecord]:
        return list(self.transfer_logs)

    def list_scenes(self) -> List[str]:
        return list(self.scenes)

    def list_sales_reps(self) -> List[str]:
        return list(self.sales_reps)

    def list_remaining_products(self) -> List[RemainingProduct]:
        items: List[RemainingProduct] = []
        for tpl in self.card_templates:
            items.append(
                RemainingProduct(
                    product_id=tpl.id,
                    name=tpl.name,
                    type="membership_card",
                    remaining=max(tpl.total - tpl.issued_count, 0),
                )
            )
        for tpl in self.coupon_templates:
            items.append(
                RemainingProduct(
                    product_id=tpl.id,
                    name=tpl.name,
                    type="coupon",
                    remaining=max(tpl.total - tpl.issued_count, 0),
                )
            )
        return items

    def list_expired_products(self) -> List[dict]:
        today = date.today()
        expired: List[dict] = []
        for member in self.members.values():
            for card in member.cards:
                if card.valid_to < today:
                    card.status = "expired"
                    expired.append({"member_id": member.id, "type": "membership_card", "id": card.id, "name": card.name})
            for coupon in member.coupons:
                if coupon.valid_to < today and coupon.status == "active":
                    coupon.status = "expired"
                if coupon.status == "expired":
                    expired.append(
                        {
                            "member_id": member.id,
                            "type": "coupon",
                            "id": coupon.id,
                            "name": coupon.name,
                        }
                    )
        return expired

    def find_verifier(self, phone: str, password: str) -> Optional[dict]:
        verifier = self.verifiers.get(phone)
        if verifier and verifier["password"] == password:
            return verifier
        return None

    def list_modification_logs(self) -> List[ValidityModificationLog]:
        return list(self.modification_logs)

    def list_cancellation_logs(self) -> List[CancellationLog]:
        return list(self.cancellation_logs)



store = InMemoryStore()
