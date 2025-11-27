# 苏宁银河国际酒店电子会员管理系统（原型）

基于 [docs/functional-requirements.md](docs/functional-requirements.md) 的需求，提供一个可运行的 API 原型，覆盖管理后台、商户核销端、会员端的核心流程，便于后续迭代。

## 快速开始

1. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```
2. 本地运行：
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```
3. 访问接口文档：启动后访问 `http://127.0.0.1:8000/docs`。

## 预览地址

启动后可直接在浏览器打开以下地址进行功能预览：

- 汇总预览：`http://127.0.0.1:8000/preview`
- 管理后台预览：`http://127.0.0.1:8000/preview/admin`
- 商户核销端预览：`http://127.0.0.1:8000/preview/merchant`
- 会员端预览：`http://127.0.0.1:8000/preview/member`

## 核心端点速览（分角色）

- `GET /health`：健康检查。
- 预览：`GET /preview` 汇总三端预览；或分别查看 `GET /preview/admin`、`/preview/merchant`、`/preview/member`。
- 管理后台
  - 会员：`GET /admin/members`、`GET /admin/members/{id}`、`POST /admin/members/{id}/cards/issue`、`POST /admin/members/{id}/coupons/issue`、`POST /admin/members/{id}/freeze`
  - 核销：`POST /admin/redemptions`
  - 产品：`GET /admin/products/card-templates`、`GET /admin/products/coupon-templates`
  - 基础数据：`GET /admin/basic/scenes`、`GET /admin/basic/sales-reps`
  - 报表：核销/转赠/库存/过期/有效期修改/注销 —— `GET /admin/reports/*`
- 商户核销端
  - 登录：`POST /merchant/login`
  - 核销：`POST /merchant/redemptions`
  - 我的核销：`GET /merchant/redemptions`
- 会员端
  - 登录：`POST /member/login/wechat`
  - 会员卡：`GET /member/cards`
  - 卡券：`GET /member/coupons`、`GET /member/coupons/{id}`
  - 转赠：`POST /member/coupons/transfer`

## 测试

```bash
python -m pytest
```

> 说明：当前实现使用内存数据模拟会员、卡券、核销记录，便于快速验证业务流程；可按需替换为数据库或第三方服务。
