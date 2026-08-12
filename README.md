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

The ETL pipeline imports generated CSV files into PostgreSQL.

Run

```bash
python app/scripts/load_data.py
```

The loader:

- Clears existing data
- Preserves foreign key relationships
- Imports tables in dependency order
- Populates all dashboard data

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

## Deployment

Backend deployed on:

- Render

Database hosted on:

- Render PostgreSQL
