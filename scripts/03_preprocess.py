import pandas as pd
from pathlib import Path


# ============================================================
# PATH
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"

PROCESSED_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# LOAD RAW DATA
# ============================================================

print("Loading raw datasets...")

stores = pd.read_csv(
    RAW_DIR / "stores.csv"
)

products = pd.read_csv(
    RAW_DIR / "products.csv"
)

sales = pd.read_csv(
    RAW_DIR / "sales.csv"
)

inventory = pd.read_csv(
    RAW_DIR / "inventory.csv"
)

calendar = pd.read_csv(
    RAW_DIR / "calendar.csv"
)


# ============================================================
# DATA PROFILING
# ============================================================

datasets = {
    "stores": stores,
    "products": products,
    "sales": sales,
    "inventory": inventory,
    "calendar": calendar,
}

for name, df in datasets.items():

    print("\n" + "=" * 60)
    print(name.upper())

    print("Shape:", df.shape)

    print("Missing:")
    print(df.isnull().sum())

    print(
        "Duplicates:",
        df.duplicated().sum()
    )


# ============================================================
# CLEAN PRODUCTS
# ============================================================

print("\nCleaning products...")

for col in [
    "Product_Cost",
    "Product_Price"
]:

    products[col] = (
        products[col]
        .astype(str)
        .str.replace(
            "$",
            "",
            regex=False
        )
        .str.strip()
        .astype(float)
    )


# ============================================================
# CLEAN DATES
# ============================================================

print("Cleaning dates...")

sales["Date"] = pd.to_datetime(
    sales["Date"],
    errors="raise"
)

stores["Store_Open_Date"] = pd.to_datetime(
    stores["Store_Open_Date"],
    errors="raise"
)

calendar["Date"] = pd.to_datetime(
    calendar["Date"],
    errors="raise"
)


# ============================================================
# CLEAN CITY
# ============================================================

stores["Store_City"] = stores[
    "Store_City"
].replace(
    {
        "Cuidad de Mexico":
        "Ciudad de Mexico"
    }
)


# ============================================================
# DIM STORE
# ============================================================

dim_store = stores.rename(
    columns={
        "Store_ID": "store_id",
        "Store_Name": "store_name",
        "Store_City": "store_city",
        "Store_Location": "store_location",
        "Store_Open_Date": "store_open_date",
    }
)


# ============================================================
# DIM CATEGORY
# ============================================================

dim_category = (
    products[
        ["Product_Category"]
    ]
    .drop_duplicates()
    .sort_values(
        "Product_Category"
    )
    .reset_index(drop=True)
)

dim_category[
    "category_id"
] = dim_category.index + 1

dim_category = dim_category.rename(
    columns={
        "Product_Category":
        "category_name"
    }
)

dim_category = dim_category[
    [
        "category_id",
        "category_name"
    ]
]

# ============================================================
# DIM PRODUCT
# ============================================================

products_normalized = products.merge(
    dim_category,
    left_on="Product_Category",
    right_on="category_name",
    how="left"
)

dim_product = products_normalized[
    [
        "Product_ID",
        "Product_Name",
        "category_id",
        "Product_Cost",
        "Product_Price",
    ]
].copy()

dim_product = dim_product.rename(
    columns={
        "Product_ID": "product_id",
        "Product_Name": "product_name",
        "Product_Cost": "product_cost",
        "Product_Price": "product_price",
    }
)


# ============================================================
# DIM DATE
# ============================================================

dim_date = calendar.copy()

dim_date["year"] = (
    dim_date["Date"].dt.year
)

dim_date["quarter"] = (
    dim_date["Date"].dt.quarter
)

dim_date["month"] = (
    dim_date["Date"].dt.month
)

dim_date["month_name"] = (
    dim_date["Date"].dt.month_name()
)

dim_date["day"] = (
    dim_date["Date"].dt.day
)

dim_date["day_of_week"] = (
    dim_date["Date"].dt.day_name()
)

dim_date = dim_date.rename(
    columns={
        "Date": "date"
    }
)


# ============================================================
# FACT SALES
# ============================================================

fact_sales = sales.rename(
    columns={
        "Sale_ID": "sale_id",
        "Date": "sale_date",
        "Store_ID": "store_id",
        "Product_ID": "product_id",
        "Units": "units",
    }
)

fact_sales = fact_sales[
    [
        "sale_id",
        "sale_date",
        "store_id",
        "product_id",
        "units",
    ]
]


# ============================================================
# FACT INVENTORY
# ============================================================

fact_inventory = inventory.rename(
    columns={
        "Store_ID": "store_id",
        "Product_ID": "product_id",
        "Stock_On_Hand":
        "stock_on_hand",
    }
)


# ============================================================
# VALIDATION
# ============================================================

print("\nValidating foreign keys...")

valid_store_ids = set(
    dim_store["store_id"]
)

valid_product_ids = set(
    dim_product["product_id"]
)

invalid_sales_store = fact_sales[
    ~fact_sales["store_id"]
    .isin(valid_store_ids)
]

invalid_sales_product = fact_sales[
    ~fact_sales["product_id"]
    .isin(valid_product_ids)
]

invalid_inventory_store = fact_inventory[
    ~fact_inventory["store_id"]
    .isin(valid_store_ids)
]

invalid_inventory_product = fact_inventory[
    ~fact_inventory["product_id"]
    .isin(valid_product_ids)
]

print(
    "Invalid sales store:",
    len(invalid_sales_store)
)

print(
    "Invalid sales product:",
    len(invalid_sales_product)
)

print(
    "Invalid inventory store:",
    len(invalid_inventory_store)
)

print(
    "Invalid inventory product:",
    len(invalid_inventory_product)
)


# ============================================================
# EXPORT PROCESSED DATA
# ============================================================

print("\nExporting processed data...")

dim_store.to_csv(
    PROCESSED_DIR /
    "dim_store.csv",
    index=False
)

dim_category.to_csv(
    PROCESSED_DIR /
    "dim_category.csv",
    index=False
)

dim_product.to_csv(
    PROCESSED_DIR /
    "dim_product.csv",
    index=False
)

dim_date.to_csv(
    PROCESSED_DIR /
    "dim_date.csv",
    index=False,
    date_format="%Y-%m-%d"
)

fact_sales.to_csv(
    PROCESSED_DIR /
    "fact_sales.csv",
    index=False,
    date_format="%Y-%m-%d"
)

fact_inventory.to_csv(
    PROCESSED_DIR /
    "fact_inventory_current.csv",
    index=False
)


print("\nPreprocessing completed.")
