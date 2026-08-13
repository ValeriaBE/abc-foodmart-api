import os
from pathlib import Path

import pandas as pd
import psycopg
from dotenv import load_dotenv

# Load environment variables so the database connection details can be read securely.
load_dotenv()

# Database connection string supplied via environment variables.
DATABASE_URL = os.getenv("DATABASE_URL")

# Folder containing the raw CSV files used to seed the database.
DATA_FOLDER = Path(__file__).resolve().parents[2] / "data"

# Ordered sequence of tables to load so foreign-key dependencies are satisfied.
TABLES = [
    "store",
    "department",
    "product_category",
    "vendor",
    "customer",
    "employee",
    "employee_schedule",
    "product",
    "store_inventory",
    "inventory_adjustment",
    "vendor_product",
    "purchase_order",
    "purchase_order_item",
    "delivery",
    "sale",
    "sale_item",
    "store_expense",
]


# Columns that should be converted to plain dates before insert.
DATE_COLUMNS = {
    "opening_date",
    "hire_date",
    "shift_date",
    "loyalty_join_date",
    "order_date",
    "expected_delivery_date",
    "expense_date",
}

# Columns that should retain a timestamp value.
DATETIME_COLUMNS = {
    "last_updated",
    "adjustment_date",
    "actual_delivery_date",
    "sale_datetime",
}

# Columns that should be stored as PostgreSQL booleans.
BOOLEAN_COLUMNS = {
    "discontinued_status",
    "is_preferred",
}


def clean_dataframe(df):
    # Normalize date, datetime, and boolean fields so the CSV data matches the database schema.

    for col in DATE_COLUMNS:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col]).dt.date

    for col in DATETIME_COLUMNS:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col])

    for col in BOOLEAN_COLUMNS:
        if col in df.columns:
            df[col] = df[col].astype(bool)

    return df


def truncate_database(conn):
    # Clear existing data before reloading to keep the database in a clean, repeatable state.

    with conn.cursor() as cur:

        cur.execute("""
        TRUNCATE TABLE

            sale_item,
            sale,
            delivery,
            purchase_order_item,
            purchase_order,
            vendor_product,
            inventory_adjustment,
            store_inventory,
            employee_schedule,
            employee,
            customer,
            vendor,
            product,
            product_category,
            department,
            store_expense,
            store

        RESTART IDENTITY CASCADE;
        """)

    conn.commit()


def insert_table(conn, table):
    # Load one CSV file into its corresponding PostgreSQL table.

    csv = DATA_FOLDER / f"{table}.csv"

    print(f"\nLoading {table}")

    if not csv.exists():
        raise FileNotFoundError(csv)

    df = pd.read_csv(csv)

    print(f"Rows: {len(df)}")

    # Convert values to the correct Python/Pandas types before bulk insert.
    df = clean_dataframe(df)

    columns = list(df.columns)

    placeholders = ", ".join(["%s"] * len(columns))

    sql = f"""
    INSERT INTO {table}
    ({", ".join(columns)})
    VALUES ({placeholders})
    """

    values = [tuple(row) for row in df.itertuples(index=False, name=None)]

    # Insert rows in bulk to speed up the load process.
    with conn.cursor() as cur:

        cur.executemany(sql, values)

    conn.commit()

    print(f"✓ Imported {table}")


def main():
    # Full seed process: clear tables, then insert each dataset in order.

    print("=" * 60)
    print("ABC FOODMART DATA LOADER")
    print("=" * 60)

    # Connect to PostgreSQL using the environment-provided URL.
    conn = psycopg.connect(DATABASE_URL)

    truncate_database(conn)

    print("Database cleared.")

    for table in TABLES:

        try:

            insert_table(conn, table)

        except Exception as e:

            conn.rollback()

            print(f"\nFAILED: {table}")

            print(e)

            break

    conn.close()

    print("\nFinished.")


if __name__ == "__main__":
    main()