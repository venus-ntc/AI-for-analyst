# Dashboard & Business Insights cho ngành bán lẻ

## 1. Mục tiêu

Phần này nghiên cứu cách lựa chọn **KPI (Key Performance Indicator)** và **loại biểu đồ** phù hợp cho Dashboard phân tích bán lẻ.

Mục tiêu của Dashboard là giúp người dùng trả lời nhanh các nhóm câu hỏi:

- Doanh nghiệp bán được bao nhiêu?
- Doanh thu và lợi nhuận đang thay đổi như thế nào?
- Category, product hoặc store nào tạo ra nhiều doanh thu?
- Sản phẩm nào bán chạy?
- Tình trạng tồn kho hiện tại như thế nào?
- Sản phẩm nào đang hết hàng?
- Có sự khác biệt về hiệu quả giữa các cửa hàng hoặc loại vị trí cửa hàng hay không?

Dashboard cũng là lớp trình bày kết quả phía trên PostgreSQL và Text-to-SQL. Vì vậy mỗi Business Insight cần có mapping rõ ràng từ:

```text
Business Question
        ↓
Business Metric / KPI
        ↓
Database Fields
        ↓
SQL Aggregation
        ↓
Visualization
```

---

# 2. Danh mục KPI cho Retail Dashboard

## 2.1. Total Revenue

### Định nghĩa

Tổng giá trị bán hàng trong khoảng thời gian được chọn.

### Công thức

```text
Revenue = Σ(Units × Product Price)
```

### Database mapping

```text
fact_sales.units
        ×
dim_product.product_price
```

### Ý nghĩa kinh doanh

Revenue phản ánh quy mô bán hàng. Đây là KPI tổng quan để theo dõi doanh thu theo thời gian, cửa hàng, thành phố, category hoặc product.

### Visualization

- KPI Card: tổng doanh thu.
- Line Chart: doanh thu theo thời gian.
- Bar Chart: doanh thu theo category/store.
- Horizontal Bar Chart: top sản phẩm theo doanh thu.

---

## 2.2. Units Sold

### Định nghĩa

Tổng số đơn vị sản phẩm đã bán.

### Công thức

```text
Units Sold = Σ Units
```

### Database mapping

```text
fact_sales.units
```

### Ý nghĩa kinh doanh

Cho biết khối lượng sản phẩm thực tế được bán ra. KPI này hữu ích khi so sánh sức tiêu thụ giữa các product hoặc category.

### Visualization

- KPI Card.
- Line Chart theo tháng.
- Bar Chart theo category.
- Horizontal Bar Chart cho Top Products.

---

## 2.3. Gross Profit

### Định nghĩa

Lợi nhuận gộp từ hoạt động bán sản phẩm, trước các chi phí vận hành khác.

### Công thức

```text
Gross Profit
= Σ[Units × (Product Price − Product Cost)]
```

### Database mapping

```text
fact_sales.units
dim_product.product_price
dim_product.product_cost
```

### Ý nghĩa kinh doanh

Giúp phân tích không chỉ bán được bao nhiêu mà còn tạo ra bao nhiêu lợi nhuận gộp.

### Visualization

- KPI Card.
- Bar Chart theo category.
- Bar Chart theo store.
- Line Chart theo thời gian.

---

## 2.4. Gross Margin

### Định nghĩa

Tỷ lệ lợi nhuận gộp trên doanh thu.

### Công thức

```text
Gross Margin
= Gross Profit / Revenue × 100%
```

### Ý nghĩa kinh doanh

Cho phép so sánh hiệu quả sinh lợi giữa các category hoặc store ngay cả khi quy mô doanh thu khác nhau.

Ví dụ:

```text
Store A:
Revenue = $100,000
Gross Profit = $20,000
Gross Margin = 20%

Store B:
Revenue = $80,000
Gross Profit = $24,000
Gross Margin = 30%
```

Do đó Revenue và Gross Margin nên được xem cùng nhau khi phân tích hiệu quả.

### Visualization

- KPI Card cho margin tổng thể.
- Bar Chart để so sánh margin giữa category/store.
- Line Chart nếu cần theo dõi margin theo thời gian.

---

## 2.5. Current Inventory

### Định nghĩa

Tổng số lượng sản phẩm hiện có trong inventory snapshot.

### Công thức

```text
Current Inventory = Σ Stock On Hand
```

### Database mapping

```text
fact_inventory_current.stock_on_hand
```

### Ý nghĩa kinh doanh

Giúp theo dõi quy mô hàng tồn kho hiện tại và hỗ trợ phát hiện các khu vực/sản phẩm có mức tồn kho bất thường.

### Visualization

- KPI Card.
- Bar Chart theo store.
- Bar Chart theo category/product.
- Table cho chi tiết.

### Lưu ý về dataset

Dataset Maven Toys cung cấp inventory hiện tại nhưng không cung cấp lịch sử inventory theo thời gian. Vì vậy Dashboard không nên tuyên bố rằng nó phân tích được xu hướng tồn kho dài hạn nếu không có thêm dữ liệu snapshot lịch sử.

---

## 2.6. Out-of-stock Count

### Định nghĩa

Số record Store–Product có:

```text
stock_on_hand = 0
```

### Ý nghĩa kinh doanh

Cho biết số trường hợp sản phẩm không còn hàng tại một cửa hàng.

### Visualization

- KPI Card.
- Table chi tiết Store/Product.
- Bar Chart theo Store hoặc Category.

### Lưu ý

Không nên coi một Store–Product không có record inventory là chắc chắn có stock bằng 0. Trong dataset hiện tại, "không có record" và "stock_on_hand = 0" là hai trạng thái khác nhau.

---

## 2.7. Inventory Value

Có thể bổ sung giá trị hàng tồn kho nếu business cần.

### Công thức

```text
Inventory Cost Value
= Σ(Stock On Hand × Product Cost)
```

### Database mapping

```text
fact_inventory_current.stock_on_hand
        ×
dim_product.product_cost
```

### Visualization

- KPI Card.
- Bar Chart theo Store.
- Bar Chart theo Category.

---

# 3. Danh mục các loại biểu đồ

## 3.1. KPI Card

### Mục đích

Hiển thị một chỉ số tổng quan quan trọng.

Ví dụ:

```text
┌─────────────────────┐
│ TOTAL REVENUE       │
│                     │
│ $14.44M             │
└─────────────────────┘
```

### Phù hợp với

- Total Revenue
- Gross Profit
- Gross Margin
- Units Sold
- Current Inventory
- Out-of-stock Count

### Không phù hợp với

Việc hiển thị quá nhiều category hoặc product cùng lúc.

---

# 4. Line Chart

### Mục đích

Theo dõi xu hướng theo thời gian.

Ví dụ:

```text
Month → Revenue
```

### Phù hợp với

- Revenue by Month
- Units Sold by Month
- Gross Profit by Month
- Gross Margin by Month

### Câu hỏi kinh doanh

> Doanh thu thay đổi như thế nào theo từng tháng?

> Tháng nào có doanh thu cao/thấp?

### Vì sao chọn Line Chart?

Trục X có thứ tự thời gian. Đường nối giữa các điểm giúp người dùng nhận biết trend, mức tăng/giảm và biến động.

### Không nên dùng

Line Chart cho các category độc lập nếu mục tiêu chính chỉ là so sánh độ lớn.

---

# 5. Bar Chart

### Mục đích

So sánh các nhóm/category rời rạc.

### Phù hợp với

- Revenue by Category
- Revenue by Store
- Profit by Category
- Units Sold by Category
- Inventory by Store

Ví dụ:

```text
Revenue by Category

Toys              █████████████
Art & Crafts      ███████
Electronics       ██████
Games             ██████
Sports            █████
```

### Câu hỏi kinh doanh

> Category nào tạo ra nhiều doanh thu nhất?

> Store nào có doanh thu cao hơn?

---

# 6. Horizontal Bar Chart

### Mục đích

Tương tự Bar Chart nhưng phù hợp hơn khi nhãn dài hoặc có nhiều nhóm.

### Phù hợp với

```text
Top 5 Products by Revenue
Top 10 Stores by Revenue
Top Products by Units Sold
```

Ví dụ:

```text
Product A    ███████████████
Product B    ████████████
Product C    █████████
Product D    ███████
Product E    █████
```

### Lý do

Tên sản phẩm thường dài. Horizontal Bar giúp đọc label dễ hơn.

---

# 7. Table

### Mục đích

Hiển thị thông tin chi tiết mà người dùng cần đọc chính xác.

### Phù hợp với

- Out-of-stock products.
- Inventory details.
- Store/Product detail.
- Query results từ Text-to-SQL.

Ví dụ:

| Store | Product | Stock |
|---|---|---:|
| Store 10 | Product A | 0 |
| Store 10 | Product B | 0 |
| Store 15 | Product C | 0 |

Table phù hợp hơn chart khi người dùng cần xác định chính xác **Store nào + Product nào + Stock bao nhiêu**.

---

# 8. Mapping Business Question → KPI → Chart

| Business Question | KPI / Metric | Database | Visualization |
|---|---|---|---|
| Tổng doanh thu là bao nhiêu? | Revenue | Sales + Product | KPI Card |
| Doanh thu thay đổi theo tháng thế nào? | Revenue | Sales + Product + Date | Line Chart |
| Category nào tạo nhiều doanh thu? | Revenue | Sales + Product + Category | Bar Chart |
| Store nào có doanh thu cao? | Revenue | Sales + Store + Product | Bar Chart |
| Sản phẩm nào bán chạy? | Units Sold | Sales + Product | Horizontal Bar |
| Tổng lợi nhuận gộp? | Gross Profit | Sales + Product | KPI Card |
| Category nào có margin cao? | Gross Margin | Sales + Product + Category | Bar Chart |
| Tồn kho hiện tại là bao nhiêu? | Stock On Hand | Inventory | KPI Card |
| Sản phẩm nào hết hàng? | Out-of-stock | Inventory + Product | Table |
| Doanh thu từng tháng năm 2023? | Revenue | Sales + Product + Date | Line Chart |
| Giá trị tồn kho theo Store? | Inventory Value | Inventory + Product + Store | Bar Chart |

---

# 9. Business Insight Catalogue cho Maven Toys

## Insight 1 — Revenue Overview

```text
KPI:
Total Revenue
```

Mục tiêu:

Theo dõi quy mô doanh thu tổng thể.

---

## Insight 2 — Revenue Trend

```text
Dimension:
Date

Metric:
Revenue
```

Visualization:

```text
Line Chart
```

Mục tiêu:

Phát hiện xu hướng tăng/giảm theo tháng.

---

## Insight 3 — Category Performance

```text
Dimension:
Category

Metric:
Revenue
Gross Profit
Units Sold
```

Visualization:

```text
Bar Chart
```

Mục tiêu:

So sánh hiệu quả giữa các nhóm sản phẩm.

---

## Insight 4 — Product Performance

```text
Dimension:
Product

Metric:
Revenue / Units Sold
```

Visualization:

```text
Horizontal Bar Chart
```

Mục tiêu:

Xác định các sản phẩm có lượng bán hoặc doanh thu cao.

---

## Insight 5 — Store Performance

```text
Dimension:
Store

Metric:
Revenue
Gross Profit
```

Visualization:

```text
Bar Chart
```

Mục tiêu:

So sánh hiệu quả giữa các cửa hàng.

---

## Insight 6 — Store Location Analysis

Dataset có thông tin:

```text
Store_Location
```

Ví dụ:

```text
Downtown
Commercial
Residential
Airport
```

Có thể phân tích:

```text
Revenue by Store Location
```

Visualization:

```text
Bar Chart
```

Mục tiêu:

Kiểm tra sự khác biệt về doanh thu giữa các loại vị trí cửa hàng.

---

## Insight 7 — Inventory Monitoring

```text
Metric:
Stock On Hand
```

Visualization:

```text
KPI Card
+
Table
+
Bar Chart
```

Mục tiêu:

Theo dõi lượng hàng tồn kho hiện tại.

---

## Insight 8 — Stockout Monitoring

```text
Condition:
stock_on_hand = 0
```

Visualization:

```text
KPI Card
+
Table
```

Mục tiêu:

Nhanh chóng xác định các trường hợp hết hàng.

---

# 10. Đề xuất bố cục Dashboard

Dashboard nên ưu tiên thông tin tổng quan ở phía trên và thông tin phân tích chi tiết ở phía dưới.

```text
┌─────────────────────────────────────────────────────────────┐
│                 RETAIL BUSINESS DASHBOARD                   │
├──────────────┬──────────────┬──────────────┬───────────────┤
│ TOTAL        │ GROSS        │ UNITS        │ CURRENT       │
│ REVENUE      │ PROFIT       │ SOLD         │ INVENTORY     │
├──────────────┴──────────────┴──────────────┴───────────────┤
│                                                             │
│                  REVENUE TREND                              │
│                     LINE                                    │
│                                                             │
├──────────────────────────────┬──────────────────────────────┤
│                              │                              │
│ REVENUE BY CATEGORY          │ TOP 5 PRODUCTS               │
│ BAR CHART                    │ HORIZONTAL BAR               │
│                              │                              │
├──────────────────────────────┴──────────────────────────────┤
│                                                             │
│                 REVENUE BY STORE                            │
│                     BAR                                     │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                  OUT-OF-STOCK PRODUCTS                      │
│                        TABLE                                │
└─────────────────────────────────────────────────────────────┘
```

---

# 11. Nguyên tắc lựa chọn biểu đồ

Có thể tóm tắt bằng bảng:

| Mục đích | Biểu đồ |
|---|---|
| Một KPI tổng quan | KPI Card |
| Trend theo thời gian | Line Chart |
| So sánh category | Bar Chart |
| Ranking Top-N | Horizontal Bar |
| Chi tiết từng record | Table |
| Thành phần của một tổng | Stacked Bar / Pie khi phù hợp |
| Quan hệ giữa hai biến số | Scatter Chart |

Trong prototype hiện tại, các loại chính cần ưu tiên là:

```text
KPI Card
Line Chart
Bar Chart
Horizontal Bar Chart
Table
```

Không cần đưa quá nhiều loại chart nếu không phục vụ một business question cụ thể.

---

# 12. Mapping với Text-to-SQL

Dashboard không hoạt động độc lập với Text-to-SQL.

Ví dụ:

### User

> Doanh thu từng category là bao nhiêu?

### Semantic Mapping

```text
Intent:
Category Revenue Analysis

Metric:
Revenue

Dimension:
Category
```

### SQL

```sql
SELECT
    c.category_name,
    SUM(
        s.units * p.product_price
    ) AS revenue
FROM fact_sales s
JOIN dim_product p
    ON s.product_id = p.product_id
JOIN dim_category c
    ON p.category_id = c.category_id
GROUP BY c.category_name
ORDER BY revenue DESC;
```

### Visualization

```text
Bar Chart
```

Flow:

```text
User Question
      ↓
Intent Detection
      ↓
Business Glossary
      ↓
Schema Mapping
      ↓
SQL Generation
      ↓
PostgreSQL
      ↓
Result
      ↓
Chart Selection
      ↓
Dashboard
```

Đây là lý do Business Insights và Business Glossary của Vân có vai trò hỗ trợ trực tiếp cho phần Text-to-SQL của hệ thống.

---

# 13. Ví dụ Business Insight từ dataset Maven Toys

Dữ liệu hiện tại cho thấy các chỉ số tổng hợp có thể sử dụng để kiểm thử Dashboard gồm:

- Sales records: khoảng 829 nghìn.
- Units Sold: khoảng 1,09 triệu.
- Revenue: khoảng 14,44 triệu USD.
- Gross Profit: khoảng 4,01 triệu USD.
- Gross Margin: khoảng 27,79%.
- Current Stock: khoảng 29,742 units.

Các con số này nên được dùng làm **baseline validation** cho Dashboard. Khi triển khai thực tế, Dashboard phải tạo lại các giá trị này từ PostgreSQL thay vì hard-code.

---

# 14. Hạn chế của Business Insights

Dataset hiện tại có một số giới hạn cần ghi rõ trong báo cáo:

### 14.1. Không có Vendor

Không có dữ liệu về nhà cung cấp nên chưa thể phân tích:

- Vendor performance.
- Vendor cost.
- Supplier lead time.

### 14.2. Không có Warehouse

Chưa thể phân tích:

- Warehouse stock.
- Warehouse transfer.
- Warehouse utilization.

### 14.3. Inventory không có lịch sử

Chỉ có snapshot inventory hiện tại.

Do đó chưa thể kết luận về:

- Inventory trend.
- Historical stockout duration.
- Inventory turnover theo thời gian.

### 14.4. Không có transaction-level discount/payment information

Không nên tự suy luận các chỉ số liên quan đến:

- Discount.
- Payment method.
- Customer lifetime value.

nếu chưa có dữ liệu tương ứng.

---

# 15. Kết luận

Nghiên cứu Business Insights cho thấy Retail Dashboard nên kết hợp ba nhóm thông tin:

```text
Sales Performance
├── Revenue
├── Units Sold
├── Gross Profit
└── Gross Margin

Product / Store Performance
├── Revenue by Category
├── Top Products
├── Revenue by Store
└── Store Location Analysis

Inventory Monitoring
├── Current Inventory
├── Inventory Value
└── Out-of-stock
```

Các KPI và visualization được lựa chọn dựa trên **business question** thay vì chọn biểu đồ trước rồi tìm dữ liệu sau.

Mô hình đề xuất cho hệ thống:

```text
Natural Language Question
          ↓
Business Intent
          ↓
Business Metric
          ↓
Database Schema
          ↓
SQL
          ↓
Query Result
          ↓
Visualization
```

Điều này giúp Dashboard không chỉ là giao diện biểu đồ mà trở thành lớp Business Intelligence kết nối trực tiếp với PostgreSQL và hệ thống Text-to-SQL.
