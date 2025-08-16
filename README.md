# 听障友好咖啡厅商品出入库系统

该仓库用于设计和实现一个面向听障员工友好的咖啡厅商品出入库管理系统。

详细的系统设计请参见 [DESIGN.md](DESIGN.md)。

## 当前进度

- 提供了基础的库存管理模块 `InventoryManager`
- 提供命令行演示界面 `main.py`
- 新增基于 Flask 的网页界面和 JSON API `webapp.py`

## 运行

```bash
python main.py
```

系统将通过纯文字菜单引导用户进行入库、出库和库存查询。

### 运行网页接口

```bash
pip install flask
python webapp.py
```

随后在浏览器访问 `http://localhost:5000/`，即可通过网页进行入库、出库并查看低库存商品。
若需要脚本访问，也可以向 `/add`、`/remove` 和 `/low-stock` 发送 JSON 请求。
`/add` 接口需要提供以下字段：
`name`、`spec`、`qty`、`production_date`、`expiry_date`、`supplier`、`purchase_date`、`invoice_number`。
