# Text-to-SQL Test Set

| ID | Question | Tables | Difficulty | Visualization |
|---|---|---|---|---|
| Q01 | Tổng số lượng sản phẩm đã bán là bao nhiêu? | fact_sales | Easy | KPI |
| Q02 | Tổng doanh thu là bao nhiêu? | fact_sales + dim_product | Easy | KPI |
| Q03 | Tổng lợi nhuận gộp là bao nhiêu? | fact_sales + dim_product | Easy | KPI |
| Q04 | Doanh thu theo từng category? | sales + product + category | Medium | Bar |
| Q05 | Doanh thu theo từng store? | sales + store + product | Medium | Bar |
| Q06 | Top 5 sản phẩm có doanh thu cao nhất? | sales + product | Medium | Horizontal Bar |
| Q07 | Doanh thu từng tháng năm 2023? | sales + product + date | Medium | Line |
| Q08 | Doanh thu Electronics năm 2023? | sales + product + category + date | Hard | KPI/Bar |
| Q09 | Sản phẩm nào hết hàng tại Store 10? | inventory + product + store | Medium | Table |
| Q10 | Inventory hiện tại của Store 20? | inventory + product | Medium | Table |
| Q11 | Lợi nhuận gộp theo category? | sales + product + category | Medium | Bar |
| Q12 | Top 5 store theo doanh thu năm 2023? | sales + product + store + date | Hard | Bar |
| Q13 | Sản phẩm nào bán nhiều nhất? | sales + product | Medium | Bar |
| Q14 | Doanh thu của từng city? | sales + store + product | Medium | Bar |
| Q15 | Store nào có doanh thu Electronics cao nhất? | sales + store + product + category | Hard | Bar |

## Quy định cho mỗi test case

Lưu thêm:

```text
Expected SQL
Expected columns
Expected result
Execution time
Pass / Fail
```

Mục tiêu là dùng cùng bộ câu hỏi để đánh giá Text-to-SQL trên các LLM khác nhau.
