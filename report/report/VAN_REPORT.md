# BÁO CÁO CÔNG VIỆC – NGUYỄN THỊ CẨM VÂN

## 1. Phạm vi công việc

Theo Meeting Minute 2, phần công việc của Nguyễn Thị Cẩm Vân gồm:

- Nghiên cứu và mô hình hóa các thực thể cốt lõi trong nghiệp vụ bán lẻ: Store, Warehouse, Category, Product, Vendor, Sales.
- Tìm kiếm và chuẩn bị tập dữ liệu mẫu bán lẻ thực tế từ Kaggle.
- Nghiên cứu pipeline nạp dữ liệu đa định dạng PDF, CSV/Excel và thiết kế kết nối database, bao gồm PostgreSQL.
- Nghiên cứu ý nghĩa các loại biểu đồ và danh mục chỉ số Dashboard/Business Insights cho ngành bán lẻ.

Phạm vi thực nghiệm của phần này tập trung vào dữ liệu Sales và Inventory của dataset Maven Toys. Dataset thực nghiệm không cung cấp Vendor và Warehouse, vì vậy hai thực thể này được giữ ở mức mô hình nghiệp vụ mở rộng, không tự tạo dữ liệu giả cho database thực nghiệm.

## 2. Lựa chọn dataset

Dataset được sử dụng là Maven Toys / Mexico Toy Sales.

Các file dữ liệu sử dụng:

```text
stores.csv
products.csv
sales.csv
inventory.csv
calendar.csv
data_dictionary.csv
```

Quy mô dữ liệu sau khi profiling:

| Dataset | Số bản ghi |
|---|---:|
| Stores | 50 |
| Products | 35 |
| Sales | 829,262 |
| Inventory | 1,593 |
| Calendar | 638 |

Dữ liệu Sales bao phủ giai đoạn 01/01/2022 đến 30/09/2023.

Quy mô 829,262 dòng Sales đủ để mô phỏng một workload phân tích bán lẻ thực tế nhưng vẫn phù hợp để chạy local bằng PostgreSQL. Khi demo không đưa toàn bộ các dòng dữ liệu vào prompt của LLM; PostgreSQL thực hiện việc truy vấn và chỉ trả về kết quả cần thiết.

## 3. Data Profiling

### 3.1. Kiểm tra cấu trúc

Các nội dung kiểm tra:

- số dòng và số cột;
- tên và kiểu dữ liệu của từng trường;
- missing values;
- duplicate records;
- tính duy nhất của khóa;
- tính hợp lệ của foreign key;
- miền giá trị và thời gian.

### 3.2. Data quality

Các bước xử lý chính:

1. Kiểm tra dữ liệu thiếu.
2. Kiểm tra duplicate.
3. Kiểm tra khóa chính.
4. Kiểm tra liên kết Store/Product giữa Sales và các bảng dimension.
5. Chuẩn hóa kiểu ngày.
6. Chuẩn hóa giá tiền.

Trong `products.csv`, các trường `Product_Cost` và `Product_Price` có thể xuất hiện dưới dạng chuỗi tiền tệ, ví dụ `$9.99`. Các trường này được chuyển thành numeric trước khi đưa vào PostgreSQL.

Các trường ngày được chuyển sang kiểu `DATE`.

Các lỗi chính tả của tên thành phố được chuẩn hóa trong dữ liệu processed; dữ liệu raw được giữ nguyên để đảm bảo khả năng truy vết.

## 4. Mô hình dữ liệu bán lẻ

### 4.1. Các entity

Mô hình nghiệp vụ tổng quát:

```text
Store
Warehouse
Category
Product
Vendor
Sales
```

Trong dataset Maven Toys, phần thực nghiệm sử dụng:

```text
Store
Category
Product
Sales
Inventory
Date
```

`Inventory` được sử dụng như dữ liệu tồn kho hiện tại.

### 4.2. Mô hình PostgreSQL

Database:

```text
retail_ai
```

Các bảng:

```text
dim_store
dim_category
dim_product
dim_date
fact_sales
fact_inventory_current
```

### 4.3. Quan hệ

```text
dim_category 1 ─── N dim_product
dim_product  1 ─── N fact_sales
dim_store    1 ─── N fact_sales
dim_date     1 ─── N fact_sales

dim_store    1 ─── N fact_inventory_current
dim_product  1 ─── N fact_inventory_current
```

### 4.4. Store

Nguồn: `stores.csv`.

Các thuộc tính:

```text
store_id
store_name
store_city
store_location
store_open_date
```

### 4.5. Category

Category được tách khỏi Product thành `dim_category` để giảm lặp dữ liệu và hỗ trợ Semantic Mapping.

### 4.6. Product

Các thuộc tính:

```text
product_id
product_name
category_id
product_cost
product_price
```

### 4.7. Sales

`fact_sales` lưu dữ liệu giao dịch:

```text
sale_id
sale_date
store_id
product_id
units
```

Doanh thu được tính:

```text
Revenue = Units × Product Price
```

Lợi nhuận gộp:

```text
Gross Profit = Units × (Product Price − Product Cost)
```

Không lưu Revenue thành một cột vật lý trong fact table để tránh lặp dữ liệu có thể tính được từ Product.

### 4.8. Inventory

`fact_inventory_current` gồm:

```text
store_id
product_id
stock_on_hand
```

Tên `current` phản ánh giới hạn của dataset: dữ liệu inventory không có lịch sử snapshot theo ngày.

Không được suy luận rằng một cặp Store–Product không có record inventory đồng nghĩa với `stock_on_hand = 0`.

## 5. Data preprocessing

Pipeline:

```text
Maven Toys CSV
       ↓
Pandas
       ↓
Data Profiling
       ↓
Cleaning
       ├── Currency
       ├── Date
       └── City
       ↓
Normalization
       ├── Category
       └── Date Dimension
       ↓
Validation
       ├── Primary Key
       └── Foreign Key
       ↓
Processed CSV
       ↓
PostgreSQL
```

Script chính:

```text
scripts/03_preprocess.py
```

Kết quả:

```text
data/processed/
├── dim_store.csv
├── dim_category.csv
├── dim_product.csv
├── dim_date.csv
├── fact_sales.csv
└── fact_inventory_current.csv
```

## 6. PostgreSQL data loading

Dữ liệu processed được nạp vào PostgreSQL database `retail_ai`.

Thứ tự load:

```text
1. dim_store
2. dim_category
3. dim_product
4. dim_date
5. fact_sales
6. fact_inventory_current
```

Thứ tự này đảm bảo các bảng dimension được tạo trước khi load các bảng fact có foreign key.

Đối với `fact_sales` với 829,262 dòng, sử dụng PostgreSQL `COPY`/bulk loading thay vì thực hiện một lệnh INSERT riêng cho từng dòng.

Script:

```text
scripts/04_load_database.py
```

## 7. Kiểm tra database

Sau khi load, kiểm tra số lượng:

```text
dim_store                  50
dim_category                5
dim_product                35
dim_date                  638
fact_sales            829,262
fact_inventory_current   1,593
```

Các business query cần kiểm tra:

- Total Units Sold.
- Total Revenue.
- Gross Profit.
- Revenue by Category.
- Revenue by Store.
- Monthly Revenue.
- Out-of-stock Products.

## 8. Business Glossary và Semantic Mapping

Một Business Glossary được chuẩn bị để hỗ trợ tầng Semantic Mapping:

| Business term | Mapping |
|---|---|
| Doanh thu | `SUM(units * product_price)` |
| Sản lượng bán | `SUM(units)` |
| Giá vốn | `SUM(units * product_cost)` |
| Lợi nhuận gộp | `SUM(units * (product_price - product_cost))` |
| Biên lợi nhuận | `gross_profit / revenue` |
| Tồn kho | `stock_on_hand` |
| Hết hàng | `stock_on_hand = 0` |
| Cửa hàng | `dim_store` |
| Danh mục | `dim_category` |
| Sản phẩm | `dim_product` |

Business Glossary giúp chuyển cách diễn đạt nghiệp vụ của người dùng thành field, bảng và công thức SQL tương ứng.

## 9. Dashboard và Business Insights

Các KPI đề xuất:

```text
Total Revenue
Gross Profit
Gross Margin
Units Sold
Current Inventory
```

Các phân tích:

```text
Revenue by Month
Revenue by Category
Revenue by Store
Top Products
Out-of-stock Products
Inventory Value
```

Gợi ý visualization:

| Business metric | Visualization |
|---|---|
| Total Revenue | KPI Card |
| Gross Profit | KPI Card |
| Gross Margin | KPI Card |
| Units Sold | KPI Card |
| Revenue by Month | Line Chart |
| Revenue by Category | Bar Chart |
| Revenue by Store | Bar Chart |
| Top Products | Horizontal Bar |
| Inventory | Table |
| Out-of-stock | Table |

## 10. Data ingestion đa định dạng

### 10.1. CSV/Excel

```text
Upload
  ↓
File Validation
  ↓
Preview
  ↓
Schema Detection
  ↓
Column Mapping
  ↓
Data Validation
  ↓
Staging
  ↓
Transformation
  ↓
PostgreSQL
```

### 10.2. PDF

```text
Upload
  ↓
Validation
  ↓
Text Extraction
  ↓
Metadata
  ↓
Chunking
  ↓
Embedding / Vector Store
```

Phần embedding, vector database và RAG thuộc luồng xử lý tri thức của hệ thống; phần công việc của Vân tập trung vào ingestion, metadata và database connectivity.

## 11. PostgreSQL connection interface

Giao diện đề xuất:

```text
+----------------------------------+
|       DATABASE CONNECTION        |
+----------------------------------+
| Database Type                    |
| [ PostgreSQL                  ]  |
|                                  |
| Host                             |
| [ localhost                   ]  |
|                                  |
| Port                             |
| [ 5432                        ]  |
|                                  |
| Database                         |
| [ retail_ai                   ]  |
|                                  |
| Username                         |
| [ postgres                    ]  |
|                                  |
| Password                         |
| [ ********                    ]  |
|                                  |
|      [ TEST CONNECTION ]         |
+----------------------------------+
```

Sau khi kết nối thành công, hệ thống có thể đọc schema và metadata của database.

## 12. Text-to-SQL test

Bộ test được thiết kế với các mức độ từ đơn giản đến nhiều bảng JOIN.

Ví dụ:

```text
Tổng doanh thu là bao nhiêu?

Doanh thu theo từng category?

Top 5 sản phẩm có doanh thu cao nhất?

Store nào có doanh thu cao nhất?

Doanh thu từng tháng năm 2023?

Doanh thu của Electronics trong năm 2023?

Sản phẩm nào hết hàng tại Store 10?

Inventory hiện tại của Store 20?
```

Mỗi test case nên lưu:

```text
Question
Expected SQL
Tables
Difficulty
Expected Result Columns
Expected Visualization
```

## 13. Kết quả bàn giao

Phần công việc đã chuẩn bị các thành phần:

1. Dataset retail thực nghiệm.
2. Data profiling và data quality checks.
3. Mô hình Retail Sales & Inventory.
4. Dimension/Fact schema cho PostgreSQL.
5. Python preprocessing pipeline.
6. PostgreSQL loading pipeline.
7. Business Glossary.
8. KPI và visualization catalogue.
9. Text-to-SQL test set.
10. Thiết kế ingestion pipeline cho CSV/Excel/PDF.
11. Thiết kế giao diện PostgreSQL connection.

## 14. Hạn chế

- Dataset không cung cấp Vendor.
- Dataset không cung cấp Warehouse.
- Inventory không có lịch sử theo thời gian.
- Không được xem missing inventory record là stock bằng 0.
- Revenue và Gross Profit được suy ra từ Units, Product Price và Product Cost.
- Các giới hạn trên cần được ghi rõ khi đánh giá hệ thống.

