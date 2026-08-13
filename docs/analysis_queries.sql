/*
============================================================
ABC Foodmart
Analytical Procedures
============================================================
*/


/*============================================================
Procedure 1
Business Question:
Which store generates the highest revenue?
============================================================*/

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



/*============================================================
Procedure 2
Business Question:
How have sales changed over time?
============================================================*/

SELECT
    DATE_TRUNC('month', s.sale_datetime) AS month,
    SUM(
        si.quantity * si.unit_price
        - COALESCE(si.discount_amount, 0)
    ) AS revenue
FROM sale s
JOIN sale_item si
    ON s.sale_id = si.sale_id
GROUP BY month
ORDER BY month;



/*============================================================
Procedure 3
Business Question:
Which product categories generate the most revenue?
============================================================*/

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
GROUP BY pc.category_name
ORDER BY revenue DESC;



/*============================================================
Procedure 4
Business Question:
Which products are the best sellers?
============================================================*/

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
LIMIT 10;



/*============================================================
Procedure 5
Business Question:
Which products require immediate restocking?
============================================================*/

SELECT
    si.inventory_id,
    st.store_name,
    p.product_name,
    p.brand,
    si.quantity_on_hand,
    si.reorder_level,
    si.aisle_number,
    si.shelf_number,
    (
        si.reorder_level
        - si.quantity_on_hand
    ) AS units_below_reorder
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



/*============================================================
Procedure 6
Business Question:
How are vendors performing?
============================================================*/

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

/*============================================================
Procedure 7
Business Question:
Which stores have the highest average transaction value?
============================================================*/

SELECT
    st.store_name,
    ROUND(
        AVG(
            (
                SELECT SUM(
                    si.quantity * si.unit_price
                    - COALESCE(si.discount_amount,0)
                )
                FROM sale_item si
                WHERE si.sale_id = s.sale_id
            )
        ),
        2
    ) AS average_transaction_value
FROM sale s
JOIN store st
    ON s.store_id = st.store_id
GROUP BY st.store_name
ORDER BY average_transaction_value DESC;

/*============================================================
Procedure 8
Business Question:
Which products sell best in each location?
============================================================*/

WITH product_sales AS (

SELECT
    st.store_name,
    p.product_name,
    SUM(
        si.quantity * si.unit_price
        - COALESCE(si.discount_amount,0)
    ) AS revenue
FROM sale s
JOIN sale_item si
    ON s.sale_id = si.sale_id
JOIN product p
    ON si.product_id = p.product_id
JOIN store st
    ON s.store_id = st.store_id
GROUP BY
    st.store_name,
    p.product_name

),
ranked AS (
SELECT *,
ROW_NUMBER() OVER(
PARTITION BY store_name
ORDER BY revenue DESC
) rn
FROM product_sales
)
SELECT
store_name,
product_name,
revenue
FROM ranked
WHERE rn=1
ORDER BY store_name;

/*============================================================
Procedure 9
Business Question:
Which days generate the most revenue?
============================================================*/

SELECT
TO_CHAR(
    s.sale_datetime,
    'Day'
) AS weekday,
SUM(
si.quantity * si.unit_price
- COALESCE(si.discount_amount,0)
) AS revenue
FROM sale s
JOIN sale_item si
ON s.sale_id=si.sale_id
GROUP BY weekday
ORDER BY revenue DESC;

/*============================================================
Procedure 10
Business Question:
Which stores have the greatest inventory investment?
============================================================*/

WITH latest_cost AS (
SELECT DISTINCT ON (poi.product_id)
    poi.product_id,
    poi.unit_cost
FROM purchase_order_item poi
JOIN purchase_order po
ON poi.purchase_order_id = po.purchase_order_id
ORDER BY
    poi.product_id,
    po.order_date DESC
)
SELECT
st.store_name,
ROUND(
SUM(
si.quantity_on_hand *
COALESCE(lc.unit_cost,0)
),
2
) AS inventory_value
FROM store_inventory si
JOIN store st
ON si.store_id = st.store_id
LEFT JOIN latest_cost lc
ON si.product_id = lc.product_id
GROUP BY st.store_name
ORDER BY inventory_value DESC;