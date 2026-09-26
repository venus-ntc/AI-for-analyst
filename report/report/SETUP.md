# Installation & Run Guide – Retail AI

## 1. Mục tiêu
- Visual Studio Code
- Python
- PostgreSQL local
- pgAdmin4 để kiểm tra database

## 2. Prerequisites

Cần có:

```text
Windows
Python 3.x
PostgreSQL
pgAdmin4
Visual Studio Code
```

Kiểm tra PostgreSQL:

```text
Win + R
→ services.msc
→ postgresql-x64-XX
```

Service phải ở trạng thái:

```text
Running
```

## 3. Project structure

```text
retail-ai/
├── .env
├── .gitignore
├── requirements.txt
│
├── data/
│   ├── raw/
│   │   ├── stores.csv
│   │   ├── products.csv
│   │   ├── sales.csv
│   │   ├── inventory.csv
│   │   ├── calendar.csv
│   │   └── data_dictionary.csv
│   │
│   └── processed/
│
├── scripts/
│   ├── 01_test_connection.py
│   ├── 02_create_database.py
│   ├── 03_preprocess.py
│   ├── 04_load_database.py
│   └── 05_validate_database.py
│
├── sql/
│   ├── 01_schema.sql
│   ├── 02_indexes.sql
│   └── 03_business_queries.sql
│
└── report/
    ├── README.md
    ├── VAN_REPORT.md
    ├── SETUP.md
    ├── BUSINESS_GLOSSARY.md
    └── TEXT_TO_SQL_TEST.md
```

## 4. Open project in VS Code

Mở:

```text
File
→ Open Folder
→ retail-ai
```

Mở Terminal:

```text
Ctrl + `
```

## 5. Create virtual environment

```powershell
python -m venv .venv
```

Activate:

```powershell
.venv\Scripts\Activate.ps1
```

Nếu PowerShell chặn:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Sau đó activate lại:

```powershell
.venv\Scripts\Activate.ps1
```

Terminal phải có:

```text
(.venv)
```

## 6. Install packages

`requirements.txt`:

```text
pandas
psycopg[binary]
python-dotenv
openpyxl
```

Cài:

```powershell
pip install -r requirements.txt
```

## 7. Configure PostgreSQL

Tạo `.env` ở thư mục gốc:

```env
PG_HOST=localhost
PG_PORT=5432
PG_USER=postgres
PG_PASSWORD=YOUR_POSTGRES_PASSWORD

PG_ADMIN_DB=postgres
PG_DATABASE=retail_ai
```

Thay `YOUR_POSTGRES_PASSWORD` bằng password PostgreSQL local.

Không commit `.env` lên Git.

`.gitignore`:

```gitignore
.venv/
.env
__pycache__/
*.pyc
```

## 8. Test PostgreSQL connection

Chạy:

```powershell
python scripts/01_test_connection.py
```

Kết quả mong đợi:

```text
PostgreSQL connection: OK
```

Nếu lỗi `Connection refused`, kiểm tra PostgreSQL service và port:

```cmd
netstat -ano | findstr :5432
```

## 9. Create database

Chạy:

```powershell
python scripts/02_create_database.py
```

Kết quả:

```text
Database 'retail_ai' created.
```

Nếu database đã tồn tại:

```text
Database 'retail_ai' already exists.
```

vẫn OK.

## 10. Prepare dataset

Đặt dataset gốc vào:

```text
data/raw/
```

Không sửa trực tiếp file trong `raw`.

## 11. Preprocess

Chạy:

```powershell
python scripts/03_preprocess.py
```

Script thực hiện:

```text
Load
→ Profiling
→ Cleaning
→ Normalization
→ Validation
→ Export
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

Kiểm tra row count:

```text
dim_store                    50
dim_category                  5
dim_product                  35
dim_date                    638
fact_sales              829,262
fact_inventory_current     1,593
```

## 12. Create PostgreSQL schema and load data

Chạy:

```powershell
python scripts/04_load_database.py
```

Script sẽ:

1. connect vào `retail_ai`;
2. tạo tables;
3. load dimensions;
4. load facts;
5. dùng PostgreSQL bulk loading (`COPY`) cho dữ liệu lớn.

Thứ tự:

```text
dim_store
dim_category
dim_product
dim_date
fact_sales
fact_inventory_current
```

## 13. Validate database

Chạy:

```powershell
python scripts/05_validate_database.py
```

Expected:

```text
dim_store                  50
dim_category                5
dim_product                35
dim_date                  638
fact_sales            829,262
fact_inventory_current 1,593
```

## 14. Create indexes

Mở:

```text
sql/02_indexes.sql
```

Chạy trong VS Code PostgreSQL extension hoặc pgAdmin.

Các index chính:

```text
fact_sales(sale_date)
fact_sales(store_id)
fact_sales(product_id)
fact_sales(store_id, sale_date)

fact_inventory_current(store_id)
fact_inventory_current(product_id)
```

## 15. Run business queries

Mở:

```text
sql/03_business_queries.sql
```

Kiểm tra:

- Total Revenue
- Gross Profit
- Revenue by Category
- Revenue by Store
- Monthly Revenue
- Out-of-stock

Không chạy:

```sql
SELECT * FROM fact_sales;
```

vì bảng có 829,262 dòng.

Nếu cần xem sample:

```sql
SELECT *
FROM fact_sales
LIMIT 100;
```

## 16. Connect from VS Code

Có thể dùng PostgreSQL extension.

Connection:

```text
Host: localhost
Port: 5432
Database: retail_ai
Username: postgres
Password: ********
```

Database tree:

```text
retail_ai
└── Schemas
    └── public
        └── Tables
            ├── dim_store
            ├── dim_category
            ├── dim_product
            ├── dim_date
            ├── fact_sales
            └── fact_inventory_current
```

## 17. pgAdmin

pgAdmin4 dùng để:

- kiểm tra PostgreSQL service;
- xem database/table;
- kiểm tra row count;
- chạy SQL;
- troubleshoot.

Không bắt buộc phải dùng pgAdmin để chạy pipeline Python.

## 18. Full run

Sau khi project đã được setup:

```powershell
.venv\Scripts\Activate.ps1

python scripts/01_test_connection.py

python scripts/02_create_database.py

python scripts/03_preprocess.py

python scripts/04_load_database.py

python scripts/05_validate_database.py
```

Sau đó:

```text
psql -h localhost -p 5432 -U postgres -d retail_ai -f "sql/02_indexes.sql"
psql -h localhost -p 5432 -U postgres -d retail_ai -f "sql/03_business_queries.sql"
```

## 19. Troubleshooting

### PostgreSQL connection refused

Kiểm tra:

```text
services.msc
→ postgresql-x64-XX
→ Running
```

và:

```cmd
netstat -ano | findstr :5432
```

### Password authentication failed

Kiểm tra `.env`:

```env
PG_USER=postgres
PG_PASSWORD=...
```

### Database does not exist

Chạy:

```powershell
python scripts/02_create_database.py
```

### Foreign key error

Kiểm tra thứ tự load:

```text
dim_store
→ dim_category
→ dim_product
→ dim_date
→ fact_sales
→ fact_inventory_current
```

### pgAdmin connection lost khi xem Sales

Không load toàn bộ:

```sql
SELECT * FROM fact_sales;
```

Dùng:

```sql
SELECT *
FROM fact_sales
LIMIT 100;
```

hoặc:

```sql
SELECT COUNT(*)
FROM fact_sales;
```
