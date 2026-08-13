# ABC Foodmart API

FastAPI backend for the ABC Foodmart Database Systems project.

The API provides analytical endpoints used by the executive dashboard and supports direct interaction with a PostgreSQL database.

---

## Technology Stack

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Psycopg
- Pandas
- Uvicorn

---

## Features

- REST API
- PostgreSQL integration
- Dashboard analytics
- Store filtering
- ETL data loading
- Database status endpoint

---

## Project Structure

```
app/
│
├── queries/
│
├── routers/
│
├── scripts/
│
├── database.py
│
└── main.py

data/

requirements.txt
```

---

## Installation

Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/abc-foodmart-api.git
```

Create a virtual environment

```bash
python -m venv .venv
```

Activate

Windows

```bash
.venv\Scripts\activate
```

Mac/Linux

```bash
source .venv/bin/activate
```

Install packages

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file

```env
DATABASE_URL=postgresql://username:password@localhost:5432/abc_foodmart
```

For deployment on Render, use the Internal Database URL provided by Render.

---

## Running the API

```bash
uvicorn app.main:app --reload
```

Swagger documentation

```
http://localhost:8000/docs
```

---

## API Endpoints

### Connection

```
GET /api/connection
```

Returns database connection status.

---

### Dashboard KPIs

```
GET /api/kpis
```

Optional

```
?store_id=1
```

---

### Revenue by Store

```
GET /api/revenue-by-store
```

---

### Monthly Sales

```
GET /api/monthly-sales
```

---

### Sales by Category

```
GET /api/category-sales
```

---

### Top Products

```
GET /api/top-products
```

---

### Inventory Alerts

```
GET /api/low-stock
```

---

### Vendor Performance

```
GET /api/vendor-performance
```

---

### Stores

```
GET /api/stores
```

Returns all store locations.

---

### Database Status

```
GET /api/database-status
```

Returns information about the connected PostgreSQL database.

---

## ETL Process

The project uses a three-stage data pipeline to prepare and populate the PostgreSQL database.

### Stage 1 – Data Generation

`app/scripts/generate_data.py`

Since no operational dataset was provided, a Python script was developed to generate realistic grocery store data based on the ABC Foodmart business scenario.

The script creates datasets for:

- Stores
- Departments
- Product Categories
- Vendors
- Customers
- Employees
- Employee Schedules
- Products
- Store Inventory
- Inventory Adjustments
- Vendor Products
- Purchase Orders
- Purchase Order Items
- Deliveries
- Sales
- Sale Items
- Store Expenses

The generated data is exported as CSV files to the `data/` directory.

Run:

```bash
python app/scripts/generate_data.py
```

---

### Stage 2 – Extract & Transform

`etl/project_checkpoint4_group1.ipynb`

The ETL notebook processes the generated data by:

- Reading the source dataset
- Cleaning and standardizing column names
- Formatting dates and times
- Handling missing values
- Standardizing categorical values
- Exporting cleaned CSV files
- Generating an ETL summary

---

### Stage 3 – Load

`app/scripts/load_data.py`

The loading script imports the cleaned CSV files into PostgreSQL.

Features include:

- Loads tables in dependency order
- Preserves primary and foreign key relationships
- Commits data to PostgreSQL
- Populates all 17 normalized tables

Run:

```bash
python app/scripts/load_data.py
```

---

## ETL Workflow

```text
Business Scenario
        ↓
generate_data.py
        ↓
Generated CSV Files
        ↓
ETL Notebook
(Clean & Transform)
        ↓
Clean CSV Files
        ↓
load_data.py
        ↓
PostgreSQL Database
        ↓
FastAPI REST API
        ↓
React Dashboard
```

---

## Database

The backend connects to a PostgreSQL database consisting of 17 normalized tables in Third Normal Form (3NF).

Core entities include:

- Store
- Product
- Product Category
- Customer
- Vendor
- Vendor Product
- Sale
- Sale Item
- Purchase Order
- Delivery
- Inventory

---

## Documentation

Project documentation is available in the `docs/` folder.

- **ERD.pdf** – Complete Entity Relationship Diagram
- **schema.sql** – SQL schema containing all CREATE TABLE statements

The database consists of 17 normalized tables in Third Normal Form (3NF), connected through primary and foreign key relationships.

---

## Deployment

Backend deployed on:

- Render

Database hosted on:

- Render PostgreSQL

# ABC Foodmart Sample Data

This folder contains the generated datasets used to populate the PostgreSQL database for the ABC Foodmart Database Systems project.

Files include:

- customer.csv
- delivery.csv
- employee.csv
- inventory_adjustment.csv
- product.csv
- product_category.csv
- purchase_order.csv
- purchase_order_item.csv
- sale.csv
- sale_item.csv
- store.csv
- store_expense.csv
- store_inventory.csv
- vendor.csv
- vendor_product.csv

These datasets were generated to simulate the daily operations of a multi-store grocery chain and support database design, ETL, and analytical reporting.