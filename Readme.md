# E-Commerce Analytics Platform

An end-to-end analytics platform built on the Olist Brazilian E-Commerce public dataset — combining internal transactional data with live currency exchange rate data, modeled through a Medallion Architecture, and delivered as a business-facing Power BI dashboard with basic sales forecasting.

**Status:** In progress — Bronze layer complete (loaded, data-quality checked). Silver layer transformation in development.

---

## Business Problem

Olist is a Brazilian e-commerce marketplace connecting small and medium sellers with customers across the platform. Leadership needs clear, reliable reporting to make decisions about growth, customer experience, and seller performance — but raw operational data is scattered across disconnected systems (orders, payments, reviews, products, sellers), with no unified reporting layer, and all financial figures are recorded only in local currency (BRL), limiting usefulness for stakeholders reporting internationally.

### Key business questions this project answers

- **Revenue & sales performance** — total revenue trends over time, top-performing product categories, and revenue converted to USD for international reporting
- **Customer behavior & satisfaction** — do delivery delays correlate with lower review scores? How does satisfaction vary by product category or region?
- **Delivery & logistics performance** — what percentage of orders arrive later than estimated, and how does this vary by seller/customer location?
- **Seller performance** — which sellers drive the most revenue, and which show consistent delivery or review-score issues?
- **Product performance** — which categories have high order volume vs. high revenue (not always the same), and which have unusually poor review rates?

The relationship between **delivery delay and review score** is the headline analytical question this project is built around — it requires joining across orders and reviews, deriving a calculated delay metric, and correlating it with satisfaction, rather than just reporting raw totals.

## Architecture

```
Raw CSVs (Olist dataset)
        │
        ▼
 Python — Extract & Load (psycopg2 COPY, bulk loading)
        │
        ▼
 PostgreSQL (Neon) — Bronze Layer
 (raw data landed as VARCHAR — no assumptions about type until cleaned)
        │
        ▼
 Python — API enrichment (live currency exchange rates)
        │
        ▼
 SQL — Transform: Bronze → Silver
 (data quality checks, TRIM/whitespace handling, correct type casting)
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

The pipeline follows an **ELT** pattern, not ETL: raw data is loaded first, and all transformation logic (Bronze → Silver → Gold) is written and executed as SQL directly inside PostgreSQL, rather than round-tripped through Python — the same approach modern data teams use with tools like dbt.

## Tech Stack

| Category | Tools |
|---|---|
| Language | Python 3.12 |
| Data loading | psycopg2 (`copy_expert` — bulk CSV loading via `COPY`) |
| Database | PostgreSQL (hosted on Neon) |
| Transformation | SQL (Bronze → Silver → Gold) |
| Data enrichment | Public currency exchange rate API |
| Analysis | pandas (EDA), basic time series forecasting |
| Reporting | Power BI (DAX, KPI dashboards) |
| Secrets management | python-dotenv |

## Dataset

[Olist Brazilian E-Commerce Public Dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) — real, anonymized order data from a Brazilian marketplace, spanning ~2 years across 9 relational tables: orders, order items, order payments, order reviews, customers, sellers, products, product category translations, and geolocation.

## Database Schema

### Bronze Layer — raw staging tables
Every column loaded as `VARCHAR`, exactly as it appears in the source CSVs — no type assumptions made until the data has been examined and cleaned. This avoids load failures caused by unexpected formatting, and keeps type-casting decisions deliberate rather than accidental.

**Data quality checks performed on Bronze:**
- Null counts across every column, distinguishing genuinely missing data (e.g., orders never delivered) from expected nulls (e.g., a review left with no written comment)
- Whitespace checks (`TRIM()` comparisons) across every column to catch leading/trailing space issues before casting to numeric or date types in Silver

### Silver Layer (in development)
Bronze data with correct data types applied, whitespace and formatting issues resolved, and deduplication performed — still one row per source record, not yet reshaped into a star schema.

### Gold Layer (planned)
- **Fact table:** grain and structure to be finalized — order-item level, joined against payments and enriched with converted currency values, including a derived delivery-delay metric
- **Dimension tables:** `dim_customer`, `dim_product` (enriched with English category names), `dim_seller`, `dim_date`
- **Reference/enrichment table:** exchange rate data from the currency API

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

- **Landing raw data as text (schema-on-read staging)** — every Bronze column is loaded as `VARCHAR`, regardless of its "true" type, so raw CSV quirks (stray whitespace, inconsistent formatting) never cause a failed load. Type casting is a deliberate Silver-layer decision, made only after examining the real data, not assumed upfront.
- **Bulk loading via `COPY`, not row-by-row inserts** — since Bronze-layer loading involves no transformation, `psycopg2`'s `copy_expert` streams each CSV directly into PostgreSQL, avoiding the network-latency cost of thousands of individual `INSERT` statements (a deliberate improvement over the row-by-row approach used in an earlier project).
- **ELT over ETL** — transformation logic (Bronze → Silver → Gold) is written in SQL and executed inside the database, not in Python, since it's more efficient for relational, join-heavy modeling than round-tripping data through pandas.
- **Business questions defined before schema design** — the Silver/Gold layer design is driven by specific analytical questions (revenue trends, delivery-delay vs. review-score correlation, seller and product performance), not by cleaning data indiscriminately. Columns without a clear connection to these questions (e.g., free-text review comments, detailed product packaging dimensions) are retained in Silver for completeness but deliberately excluded from the Gold-layer star schema.
- **Physical tables at every layer, not views** — since the source dataset is a static, one-time historical snapshot, views would offer no freshness benefit and would force Power BI to recompute expensive joins on every query; materialized tables are the correct choice for both accuracy and dashboard performance here.
- **API enrichment as a genuine business need** — since order values are recorded in BRL, converting revenue to USD via a live exchange rate API reflects a real reporting requirement for international stakeholders, not an artificially added feature.

## Future Improvements

- Automate the pipeline on a schedule using GitHub Actions
- Rebuild Silver/Gold transformations in dbt for version-controlled, tested transformation logic
- Add automated data quality tests at each layer
- Publish the Power BI dashboard to Power BI Service
- Explore sentiment analysis on free-text review comments as a future extension

## Author

**Krish Chaurasia**
[GitHub](https://github.com/Krishchaurasia05) | [LinkedIn](https://linkedin.com/in/krishchaurasia)
