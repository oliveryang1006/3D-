# 听障友好咖啡厅商品出入库系统

该仓库用于设计和实现一个面向听障员工友好的咖啡厅商品出入库管理系统。

详细的系统设计请参见 [DESIGN.md](DESIGN.md)。

## 当前进度

- 提供了基础的库存管理模块 `InventoryManager`
- 提供命令行演示界面 `main.py`
- 新增基于 Flask 的简单网页接口 `webapp.py`

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

随后在浏览器或使用 `curl` 等工具访问 `http://localhost:5000`。
