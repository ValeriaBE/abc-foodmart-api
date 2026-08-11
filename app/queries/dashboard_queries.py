from app.database import get_connection


def get_database_connection_info():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT
                    current_database() AS database_name,
                    current_user AS database_user,
                    version() AS postgres_version;
            """)

            database = cur.fetchone()

            cur.execute("""
                SELECT COUNT(*) AS table_count
                FROM information_schema.tables
                WHERE table_schema = 'public'
                  AND table_type = 'BASE TABLE';
            """)

            tables = cur.fetchone()

            cur.execute("""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
                  AND table_type = 'BASE TABLE'
                ORDER BY table_name;
            """)

            table_list = cur.fetchall()

    return {
        "status": "connected",
        "database": database["database_name"],
        "database_user": database["database_user"],
        "table_count": tables["table_count"],
        "tables": [row["table_name"] for row in table_list],
    }


def get_kpis(store_id=None):
    with get_connection() as conn:
        with conn.cursor() as cur:

            # Revenue + transaction count
            cur.execute("""
                SELECT
                    COALESCE(
                        SUM(
                            (si.quantity * si.unit_price)
                            - COALESCE(si.discount_amount, 0)
                        ),
                        0
                    ) AS total_revenue,

                    COUNT(DISTINCT s.sale_id) AS total_sales

                FROM sale s
                JOIN sale_item si
                    ON s.sale_id = si.sale_id

            """)

            sales = cur.fetchone()

            # Low stock
            cur.execute("""
                SELECT COUNT(*) AS low_stock_products
                FROM store_inventory
                WHERE quantity_on_hand <= reorder_level
            """)

            inventory = cur.fetchone()

            # Loyalty customers who have actually made purchases
            cur.execute("""
                SELECT COUNT(DISTINCT s.customer_id) AS active_customers
                FROM sale s
                WHERE s.customer_id IS NOT NULL
            """)

            customers = cur.fetchone()

    return {
        "total_revenue": sales["total_revenue"],
        "total_sales": sales["total_sales"],
        "low_stock_products": inventory["low_stock_products"],
        "active_customers": customers["active_customers"],
    }


def get_revenue_by_store():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT
                    st.store_id,
                    st.store_name,

                    COALESCE(
                        SUM(
                            (si.quantity * si.unit_price)
                            - COALESCE(si.discount_amount, 0)
                        ),
                        0
                    ) AS revenue

                FROM store st

                LEFT JOIN sale s
                    ON st.store_id = s.store_id

                LEFT JOIN sale_item si
                    ON s.sale_id = si.sale_id

                GROUP BY
                    st.store_id,
                    st.store_name

                ORDER BY revenue DESC;
            """)

            return cur.fetchall()


def get_monthly_sales(store_id=None):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT
                    DATE_TRUNC('month', s.sale_datetime)::date AS month,

                    COUNT(DISTINCT s.sale_id) AS transactions,

                    COALESCE(
                        SUM(
                            (si.quantity * si.unit_price)
                            - COALESCE(si.discount_amount, 0)
                        ),
                        0
                    ) AS revenue

                FROM sale s

                JOIN sale_item si
                    ON s.sale_id = si.sale_id

                GROUP BY
                    DATE_TRUNC('month', s.sale_datetime)

                ORDER BY month;
            """)

            return cur.fetchall()


def get_category_sales(store_id=None):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT
                    pc.category_id,
                    pc.category_name,

                    SUM(si.quantity) AS units_sold,

                    SUM(
                        (si.quantity * si.unit_price)
                        - COALESCE(si.discount_amount, 0)
                    ) AS revenue

                FROM sale_item si

                JOIN sale s
                    ON si.sale_id = s.sale_id

                JOIN product p
                    ON si.product_id = p.product_id

                JOIN product_category pc
                    ON p.category_id = pc.category_id

                GROUP BY
                    pc.category_id,
                    pc.category_name

                ORDER BY revenue DESC;
            """)

            return cur.fetchall()


def get_top_products(store_id=None, limit=10):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT
                    p.product_id,
                    p.product_name,
                    p.brand,

                    SUM(si.quantity) AS units_sold,

                    SUM(
                        (si.quantity * si.unit_price)
                        - COALESCE(si.discount_amount, 0)
                    ) AS revenue

                FROM sale_item si

                JOIN sale s
                    ON si.sale_id = s.sale_id

                JOIN product p
                    ON si.product_id = p.product_id

                GROUP BY
                    p.product_id,
                    p.product_name,
                    p.brand

                ORDER BY units_sold DESC

                LIMIT %s;
            """, (limit,))

            return cur.fetchall()


def get_low_stock(store_id=None):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT
                    si.inventory_id,
                    st.store_id,
                    st.store_name,
                    p.product_id,
                    p.product_name,
                    p.brand,
                    si.quantity_on_hand,
                    si.reorder_level,
                    si.aisle_number,
                    si.shelf_number,

                    (si.reorder_level - si.quantity_on_hand)
                        AS units_below_reorder

                FROM store_inventory si

                JOIN store st
                    ON si.store_id = st.store_id

                JOIN product p
                    ON si.product_id = p.product_id

                WHERE si.quantity_on_hand <= si.reorder_level

                ORDER BY
                    units_below_reorder DESC,
                    st.store_name,
                    p.product_name;
            """)

            return cur.fetchall()


def get_vendor_performance():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT
                    v.vendor_id,
                    v.vendor_name,

                    COUNT(DISTINCT po.purchase_order_id)
                        AS total_orders,

                    COUNT(d.delivery_id)
                        AS total_deliveries,

                    COUNT(d.delivery_id)
                        FILTER (
                            WHERE d.actual_delivery_date::date
                                  <= po.expected_delivery_date
                        ) AS on_time_deliveries,

                    COUNT(d.delivery_id)
                        FILTER (
                            WHERE d.actual_delivery_date::date
                                  > po.expected_delivery_date
                        ) AS late_deliveries,

                    ROUND(
                        AVG(
                            d.actual_delivery_date::date
                            - po.expected_delivery_date
                        ),
                        2
                    ) AS average_days_from_expected

                FROM vendor v

                LEFT JOIN purchase_order po
                    ON v.vendor_id = po.vendor_id

                LEFT JOIN delivery d
                    ON po.purchase_order_id = d.purchase_order_id

                GROUP BY
                    v.vendor_id,
                    v.vendor_name

                ORDER BY
                    late_deliveries DESC,
                    v.vendor_name;
            """)

            return cur.fetchall()