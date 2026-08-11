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


def get_database_status():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT COUNT(*) AS table_count
                FROM information_schema.tables
                WHERE table_schema = 'public'
                  AND table_type = 'BASE TABLE';
            """)
            table_count = cur.fetchone()["table_count"]

            cur.execute("""
                SELECT COALESCE(SUM(c.reltuples), 0)::BIGINT AS rows
                FROM pg_class c
                JOIN pg_namespace n
                    ON n.oid = c.relnamespace
                WHERE c.relkind = 'r'
                  AND n.nspname = 'public';
            """)
            total_rows = cur.fetchone()["rows"]

            return {
                "status": "Connected",
                "database": conn.info.dbname,
                "host": conn.info.host,
                "port": conn.info.port,
                "tables": table_count,
                "rows": total_rows,
            }


def get_kpis(store_id=None):
    with get_connection() as conn:
        with conn.cursor() as cur:

            # Revenue + transaction count
            query = """
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
            """

            params = []

            if store_id is not None:
                query += " WHERE s.store_id = %s"
                params.append(store_id)

            cur.execute(query, params)
            sales = cur.fetchone()

            # Low stock
            query = """
                SELECT COUNT(*) AS low_stock_products
                FROM store_inventory
                WHERE quantity_on_hand <= reorder_level
            """

            params = []

            if store_id is not None:
                query += " AND store_id = %s"
                params.append(store_id)

            cur.execute(query, params)
            inventory = cur.fetchone()

            # Active customers
            query = """
                SELECT COUNT(DISTINCT customer_id) AS active_customers
                FROM sale
                WHERE customer_id IS NOT NULL
            """

            params = []

            if store_id is not None:
                query += " AND store_id = %s"
                params.append(store_id)

            cur.execute(query, params)
            customers = cur.fetchone()

    return {
        "total_revenue": sales["total_revenue"],
        "total_sales": sales["total_sales"],
        "low_stock_products": inventory["low_stock_products"],
        "active_customers": customers["active_customers"],
    }


def get_revenue_by_store(store_id=None):
    with get_connection() as conn:
        with conn.cursor() as cur:

            query = """
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
            """

            params = []

            if store_id is not None:
                query += " WHERE st.store_id = %s"
                params.append(store_id)

            query += """
                GROUP BY
                    st.store_id,
                    st.store_name
                ORDER BY revenue DESC;
            """

            cur.execute(query, params)
            return cur.fetchall()


def get_monthly_sales(store_id=None):
    with get_connection() as conn:
        with conn.cursor() as cur:

            query = """
                SELECT
                    DATE_TRUNC('month', s.sale_datetime) AS month,
                    SUM(
                        si.quantity * si.unit_price
                        - COALESCE(si.discount_amount, 0)
                    ) AS revenue
                FROM sale s
                JOIN sale_item si
                    ON s.sale_id = si.sale_id
            """

            params = []

            if store_id is not None:
                query += " WHERE s.store_id = %s"
                params.append(store_id)

            query += """
                GROUP BY month
                ORDER BY month;
            """

            cur.execute(query, params)
            return cur.fetchall()


def get_category_sales(store_id=None):
    with get_connection() as conn:
        with conn.cursor() as cur:

            query = """
                SELECT
                    pc.category_name,
                    ROUND(
                        SUM(
                            si.quantity * si.unit_price
                            - COALESCE(si.discount_amount, 0)
                        ),
                        2
                    ) AS revenue
                FROM sale_item si
                JOIN sale s
                    ON s.sale_id = si.sale_id
                JOIN product p
                    ON p.product_id = si.product_id
                JOIN product_category pc
                    ON pc.category_id = p.category_id
            """

            params = []

            if store_id is not None:
                query += " WHERE s.store_id = %s"
                params.append(store_id)

            query += """
                GROUP BY pc.category_name
                ORDER BY revenue DESC;
            """

            cur.execute(query, params)
            return cur.fetchall()


def get_top_products(store_id=None, limit=10):
    with get_connection() as conn:
        with conn.cursor() as cur:

            query = """
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
            """

            params = []

            if store_id is not None:
                query += " WHERE s.store_id = %s"
                params.append(store_id)

            query += """
                GROUP BY
                    p.product_id,
                    p.product_name,
                    p.brand
                ORDER BY units_sold DESC
                LIMIT %s;
            """

            params.append(limit)

            cur.execute(query, params)
            return cur.fetchall()


def get_low_stock(store_id=None):
    with get_connection() as conn:
        with conn.cursor() as cur:

            query = """
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
            """

            params = []

            if store_id is not None:
                query += " AND si.store_id = %s"
                params.append(store_id)

            query += """
                ORDER BY
                    units_below_reorder DESC,
                    st.store_name,
                    p.product_name;
            """

            cur.execute(query, params)
            return cur.fetchall()


def get_vendor_performance(store_id=None):
    with get_connection() as conn:
        with conn.cursor() as cur:

            query = """
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
            """

            params = []

            if store_id is not None:
                query += " WHERE po.store_id = %s"
                params.append(store_id)

            query += """
                GROUP BY
                    v.vendor_id,
                    v.vendor_name
                ORDER BY
                    late_deliveries DESC,
                    v.vendor_name;
            """

            cur.execute(query, params)
            return cur.fetchall()


def get_stores():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT
                    store_id,
                    store_name
                FROM store
                ORDER BY store_name;
            """)

            return cur.fetchall()