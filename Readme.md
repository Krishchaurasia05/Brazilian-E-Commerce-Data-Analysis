cat > /mnt/user-data/outputs/README.md << 'EOF'
# E-Commerce Analytics Platform

An end-to-end analytics platform built on the Olist Brazilian E-Commerce public dataset — combining internal transactional data with live currency exchange rate data, modeled through a Medallion Architecture, and delivered as a business-facing Power BI dashboard with basic sales forecasting.

**Status:** In progress — Bronze layer (Extract & Load) complete, Silver/Gold transformation, API enrichment, EDA/forecasting, and Power BI reporting in development.

---

## Business Problem

An e-commerce marketplace operating across Brazil needs reliable, business-ready reporting on sales performance, customer behavior, and product trends — but its raw operational data is spread across multiple disconnected systems (orders, payments, products, sellers, reviews) and recorded only in local currency (BRL). Stakeholders reporting internationally need this converted and modeled into something they can actually act on.

## Architecture

```
Raw CSVs (Olist dataset)
        │
        ▼
 Python — Extract & Load (psycopg2 COPY)
        │
        ▼
 PostgreSQL (Neon) — Bronze Layer (raw, unmodified staging tables)
        │
        ▼
 Python — API enrichment (live currency exchange rates)
        │
        ▼
 SQL — Transform: Bronze → Silver (cleaning, type-casting, deduplication)
        │
        ▼
 SQL — Transform: Silver → Gold (star schema: fact/dimension tables)
        │
        ▼
   ┌────┴────┐
   ▼         ▼
Python EDA   Power BI
& Forecasting  Dashboard
(reads Gold)  (reads Gold)
```

The pipeline follows a strict **ELT** pattern rather than ETL: raw data is loaded first, and all transformation logic (Bronze → Silver → Gold) is written and executed as SQL directly inside PostgreSQL, rather than round-tripped through Python.

## Tech Stack

| Category | Tools |
|---|---|
| Language | Python 3.12 |
| Data loading | psycopg2 (`copy_expert` — bulk CSV loading) |
| Database | PostgreSQL (hosted on Neon) |
| Transformation | SQL (Bronze → Silver → Gold) |
| Data enrichment | Public currency exchange rate API |
| Analysis | pandas (EDA), basic time series forecasting |
| Reporting | Power BI (DAX, KPI dashboards) |
| Secrets management | python-dotenv |
| Documentation | Draw.io (ER diagrams, architecture) |

## Dataset

[Olist Brazilian E-Commerce Public Dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) — real, anonymized order data from a Brazilian marketplace, spanning ~2 years across 9 relational tables: orders, order items, order payments, order reviews, customers, sellers, products, product category translations, and geolocation.

## Database Schema

### Bronze Layer (raw staging tables)
Mirrors the original CSV structure exactly, loaded as-is via `COPY` — no transformation, no cleaning. Tables: `customers`, `geolocation`, `order_items`, `order_payments`, `orders_reviews`, `orders`, `product_cat_tran_eng`, `products`, `sellers`.

### Silver Layer (cleaned, standardized)
Bronze data with type casting, deduplication, null handling, and standardization applied — still one row per source record, not yet reshaped into a star schema.

### Gold Layer (star schema, business-ready)
- **Fact table:** grain and structure to be finalized — one row per order item, joined against payments and enriched with converted currency values
- **Dimension tables:** `dim_customer`, `dim_product` (enriched with English category names), `dim_seller`, `dim_date`
- **Reference/enrichment table:** exchange rate data from the currency API

*(Full DDL to be added to `sql/` as each layer is finalized.)*

## Project Structure

```
ecommerce-analytics-platform/
├── Dataset/                 # Raw Olist CSVs (not committed — see .gitignore)
├── sql/
│   ├── bronze/              # Staging table DDL
│   ├── silver/              # Silver transformation scripts
│   └── gold/                # Star schema build scripts
├── src/
│   ├── EL.py                # Extract & Load — raw CSVs into Bronze via COPY
│   ├── enrich_api.py         # Currency exchange rate API ingestion (planned)
│   ├── eda.py                # Exploratory data analysis (planned)
│   └── forecast.py           # Sales forecasting (planned)
├── powerbi/
│   └── ecommerce_dashboard.pbix   # (planned)
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Installation

1. Clone this repository
2. Create and activate a virtual environment, then install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Download the Olist dataset from Kaggle and place the CSVs in `Dataset/`
4. Copy `.env.example` to `.env` and fill in your Neon database credentials
5. Create the Bronze layer tables in Neon (see `sql/bronze/`)
6. Run the Extract & Load step:
   ```bash
   python src/EL.py
   ```

## Key Engineering Decisions

- **ELT over ETL** — transformation logic (Bronze → Silver → Gold) is written in SQL and executed inside the database, not in Python, since it's more efficient for relational, join-heavy modeling than round-tripping data through pandas.
- **Bulk loading via `COPY`, not row-by-row inserts** — since Bronze-layer loading involves no transformation, `psycopg2`'s `copy_expert` streams each CSV directly into PostgreSQL, avoiding the network-latency cost of thousands of individual `INSERT` statements (a deliberate improvement over the row-by-row approach used in an earlier project).
- **Physical tables at every layer, not views** — since the source dataset is a static, one-time historical snapshot, views would offer no freshness benefit and would force Power BI to recompute expensive joins on every query; materialized tables are the correct choice for both accuracy and dashboard performance here.
- **API enrichment as a real business need, not a bolted-on feature** — since order values are recorded in BRL, converting revenue to USD via a live exchange rate API reflects a genuine reporting requirement for international stakeholders.

## Future Improvements

- Automate the pipeline on a schedule using GitHub Actions
- Rebuild Silver/Gold transformations in dbt for version-controlled, tested transformation logic
- Add automated data quality tests at each layer
- Publish the Power BI dashboard to Power BI Service

## Author

**Krish Chaurasia**
[GitHub](https://github.com/Krishchaurasia05) | [LinkedIn](https://linkedin.com/in/krishchaurasia)
EOF