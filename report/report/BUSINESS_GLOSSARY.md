# Business Glossary

| Term | Definition | Database mapping |
|---|---|---|
| Doanh thu | Giá trị bán hàng | `SUM(units * product_price)` |
| Sản lượng bán | Tổng số unit đã bán | `SUM(units)` |
| Giá vốn | Chi phí hàng đã bán | `SUM(units * product_cost)` |
| Lợi nhuận gộp | Doanh thu trừ giá vốn | `SUM(units * (product_price - product_cost))` |
| Biên lợi nhuận | Lợi nhuận gộp chia doanh thu | `gross_profit / revenue` |
| Cửa hàng | Điểm bán | `dim_store` |
| Sản phẩm | Sản phẩm bán | `dim_product` |
| Danh mục | Nhóm sản phẩm | `dim_category` |
| Tồn kho | Số lượng tồn ở snapshot hiện tại | `stock_on_hand` |
| Hết hàng | Inventory record có stock bằng 0 | `stock_on_hand = 0` |
| Ngày bán | Ngày giao dịch | `fact_sales.sale_date` |
| Store ID | Định danh cửa hàng | `fact_sales.store_id` |
| Product ID | Định danh sản phẩm | `fact_sales.product_id` |

## Semantic mapping examples

### "Doanh thu"

```text
Doanh thu
→ Revenue
→ units × product_price
→ fact_sales JOIN dim_product
```

### "Lợi nhuận"

```text
Lợi nhuận
→ Gross Profit
→ units × (product_price - product_cost)
→ fact_sales JOIN dim_product
```

### "Hết hàng"

```text
Hết hàng
→ stock_on_hand = 0
→ fact_inventory_current
```
