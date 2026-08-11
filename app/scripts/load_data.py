import os
from pathlib import Path

import pandas as pd
import psycopg
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

DATA_FOLDER = Path(__file__).resolve().parents[2] / "data"

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


DATE_COLUMNS = {
    "opening_date",
    "hire_date",
    "shift_date",
    "loyalty_join_date",
    "order_date",
    "expected_delivery_date",
    "expense_date",
}

DATETIME_COLUMNS = {
    "last_updated",
    "adjustment_date",
    "actual_delivery_date",
    "sale_datetime",
}

BOOLEAN_COLUMNS = {
    "discontinued_status",
    "is_preferred",
}


def clean_dataframe(df):

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

    csv = DATA_FOLDER / f"{table}.csv"

    print(f"\nLoading {table}")

    if not csv.exists():
        raise FileNotFoundError(csv)

    df = pd.read_csv(csv)

    print(f"Rows: {len(df)}")

    df = clean_dataframe(df)

    columns = list(df.columns)

    placeholders = ", ".join(["%s"] * len(columns))

    sql = f"""
    INSERT INTO {table}
    ({", ".join(columns)})
    VALUES ({placeholders})
    """

    values = [tuple(row) for row in df.itertuples(index=False, name=None)]

    with conn.cursor() as cur:

        cur.executemany(sql, values)

    conn.commit()

    print(f"✓ Imported {table}")


def main():

    print("=" * 60)
    print("ABC FOODMART DATA LOADER")
    print("=" * 60)

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