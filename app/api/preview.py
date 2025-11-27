from fastapi import APIRouter

router = APIRouter(prefix="/preview", tags=["preview"])


def _preview_block(title: str, highlights: list[str], endpoints: list[str]):
    return {"title": title, "highlights": highlights, "endpoints": endpoints}


@router.get("/admin")
def preview_admin():
    """展示管理后台的核心能力，覆盖需求文档中的全部业务模块。"""

    return {
        "audience": "管理后台",
        "sections": [
            _preview_block(
                "会员管理",
                [
                    "会员列表：手机号/姓名/等级/注册时间筛选，查看详情、卡券、核销、消费、转赠记录",
                    "会员操作：发放/冻结会员卡",
                ],
                [
                    "GET /admin/members",
                    "GET /admin/members/{id}",
                    "POST /admin/members/{id}/cards/issue",
                    "POST /admin/members/{id}/coupons/issue",
                    "POST /admin/members/{id}/freeze",
                ],
            ),
            _preview_block(
                "卡券核销",
                ["统一核销台：扫码/输入券码，管理员可手动核销任意会员券"],
                ["POST /admin/redemptions"],
            ),
            _preview_block(
                "产品管理",
                [
                    "会员卡设置：创建/发放 1988/2688/2888 卡，配置名称、图标、价格、有效期、折扣权益",
                    "券包设置：满减、代金、房型升级等券，支持类型、面值、门槛、有效期、总量、限领数",
                ],
                ["GET /admin/products/card-templates", "GET /admin/products/coupon-templates"],
            ),
            _preview_block(
                "基础数据",
                ["场景维护：中餐厅/西餐厅/前台/康体中心等核销点管理", "核销员账户和销售人员管理"],
                ["GET /admin/basic/scenes", "GET /admin/basic/sales-reps"],
            ),
            _preview_block(
                "报表查询",
                [
                    "核销记录、转赠记录报表，可按日期/场景/核销员/券类型筛选导出",
                    "剩余、过期产品报表，统计未发放/未使用库存及已过期明细",
                    "有效期修改、注销操作日志报表，记录操作人、时间、修改前后值",
                ],
                [
                    "GET /admin/reports/redemptions",
                    "GET /admin/reports/transfers",
                    "GET /admin/reports/remaining-products",
                    "GET /admin/reports/expired-products",
                    "GET /admin/reports/modifications",
                    "GET /admin/reports/cancellations",
                ],
            ),
            _preview_block(
                "系统管理",
                ["用户/角色/菜单配置，核销员权限关联，操作日志记录"],
                ["GET /admin/basic/sales-reps"],
            ),
        ],
    }


@router.get("/merchant")
def preview_merchant():
    """展示商户核销端关键流程。"""

    return {
        "audience": "商户核销端",
        "sections": [
            _preview_block(
                "登录与场景",
                ["手机号+密码登录", "核销前强制选择所属场景（部门）"],
                ["POST /merchant/login"],
            ),
            _preview_block(
                "核销工作台",
                ["扫码或手输券码核销会员券", "核销员仅能查看本人核销记录"],
                ["POST /merchant/redemptions", "GET /merchant/redemptions"],
            ),
        ],
    }


@router.get("/member")
def preview_member():
    """展示会员端功能分区。"""

    return {
        "audience": "会员端",
        "sections": [
            _preview_block(
                "微信一键登录",
                ["授权微信手机号自动注册/绑定会员"],
                ["POST /member/login/wechat"],
            ),
            _preview_block(
                "我的会员卡/卡券",
                ["查看卡面、等级、卡号、有效期", "未使用/已使用/已过期标签页"],
                ["GET /member/cards", "GET /member/coupons"],
            ),
            _preview_block(
                "转赠与券码详情",
                ["点击任意卡券查看使用详情、核销二维码及券码", "对可转赠券生成赠卡海报/链接，转赠后记录留痕"],
                ["GET /member/coupons/{id}", "POST /member/coupons/transfer"],
            ),
            _preview_block(
                "个人中心",
                ["编辑姓名等基础信息，查看积分明细与消费记录"],
                ["GET /member/profile (预留)", "GET /member/points (预留)"],
            ),
        ],
    }


@router.get("")
def preview_all():
    """便于产品/业务评审的一站式预览，仍按角色分区展示。"""

    return {
        "admin": preview_admin(),
        "merchant": preview_merchant(),
        "member": preview_member(),
    }
