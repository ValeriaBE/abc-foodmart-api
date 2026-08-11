from pathlib import Path
from datetime import datetime, timedelta
import random

import pandas as pd


random.seed(42)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_FOLDER = PROJECT_ROOT / "data"

DATA_FOLDER.mkdir(exist_ok=True)


# --------------------------------------------------
# Helpers
# --------------------------------------------------

def save_csv(name, rows, columns):
    df = pd.DataFrame(rows, columns=columns)
    path = DATA_FOLDER / f"{name}.csv"
    df.to_csv(path, index=False)
    print(f"✓ {name}.csv -> {len(df)} rows")
    return df


def weighted_store():
    # Flushing strongest, Astoria second,
    # Williamsburg growing, Bayside/PS smaller
    return random.choices(
        [1, 2, 3, 4, 5],
        weights=[24, 34, 14, 17, 11],
        k=1,
    )[0]


def employee_for_store(employee_df, store_id):
    employees = employee_df[
        employee_df["store_id"] == store_id
    ]["employee_id"].tolist()

    return random.choice(employees)


# --------------------------------------------------
# Store
# --------------------------------------------------

store_rows = [
    [
        1,
        "Astoria Market",
        "31-01 Steinway St",
        "Queens",
        "NY",
        "11103",
        "718-555-1001",
        "2020-01-01",
        "Open",
    ],
    [
        2,
        "Flushing Market",
        "136-20 Roosevelt Ave",
        "Queens",
        "NY",
        "11354",
        "718-555-1002",
        "2020-03-01",
        "Open",
    ],
    [
        3,
        "Bayside Market",
        "212-15 Northern Blvd",
        "Queens",
        "NY",
        "11361",
        "718-555-1003",
        "2021-02-01",
        "Open",
    ],
    [
        4,
        "Williamsburg Market",
        "249 Bedford Ave",
        "Brooklyn",
        "NY",
        "11211",
        "718-555-1004",
        "2025-01-15",
        "Open",
    ],
    [
        5,
        "Park Slope Market",
        "350 5th Ave",
        "Brooklyn",
        "NY",
        "11215",
        "718-555-1005",
        "2025-03-01",
        "Open",
    ],
]

store_df = save_csv(
    "store",
    store_rows,
    [
        "store_id",
        "store_name",
        "street_address",
        "city",
        "state",
        "zip_code",
        "phone",
        "opening_date",
        "operating_status",
    ],
)


# --------------------------------------------------
# Department
# --------------------------------------------------

departments = [
    "Produce",
    "Dairy",
    "Bakery",
    "Meat",
    "Frozen",
    "Beverages",
    "Household",
    "Pharmacy",
]

department_rows = [
    [i + 1, name, f"{name} department"]
    for i, name in enumerate(departments)
]

department_df = save_csv(
    "department",
    department_rows,
    [
        "department_id",
        "department_name",
        "description",
    ],
)


# --------------------------------------------------
# Product Category
# --------------------------------------------------

categories = [
    "Produce",
    "Dairy",
    "Bakery",
    "Meat",
    "Frozen",
    "Beverages",
    "Snacks",
    "Household",
    "Personal Care",
    "Pantry",
]

category_rows = [
    [i + 1, name, f"{name} products"]
    for i, name in enumerate(categories)
]

category_df = save_csv(
    "product_category",
    category_rows,
    [
        "category_id",
        "category_name",
        "category_description",
    ],
)


# --------------------------------------------------
# Vendor
# --------------------------------------------------

vendor_names = [
    "Queens Fresh Produce",
    "Empire Dairy",
    "Metro Wholesale Foods",
    "Brooklyn Bakery Supply",
    "Atlantic Beverage",
    "Fresh Farms NY",
    "Northeast Grocery Distribution",
    "Green Valley Organics",
    "City Household Supply",
    "Prime Pantry Distribution",
]

vendor_rows = []

for vendor_id, vendor_name in enumerate(
    vendor_names,
    start=1,
):
    vendor_rows.append(
        [
            vendor_id,
            vendor_name,
            f"Representative {vendor_id}",
            f"718-555-{2000 + vendor_id}",
            f"vendor{vendor_id}@abcfoodmart.com",
            f"{100 + vendor_id} Commerce Ave",
            "New York",
            "NY",
            "10001",
            "Active",
        ]
    )

vendor_df = save_csv(
    "vendor",
    vendor_rows,
    [
        "vendor_id",
        "vendor_name",
        "contact_name",
        "phone",
        "email",
        "street_address",
        "city",
        "state",
        "zip_code",
        "vendor_status",
    ],
)


# --------------------------------------------------
# Customer
# --------------------------------------------------

customer_rows = []

for customer_id in range(1, 701):
    customer_rows.append(
        [
            customer_id,
            f"Customer{customer_id}",
            f"Last{customer_id}",
            f"customer{customer_id}@example.com",
            f"917-555-{customer_id:04d}",
            "2025-01-01",
            random.randint(0, 6000),
            "Active",
        ]
    )

customer_df = save_csv(
    "customer",
    customer_rows,
    [
        "customer_id",
        "first_name",
        "last_name",
        "email",
        "phone",
        "loyalty_join_date",
        "loyalty_points",
        "membership_status",
    ],
)


# --------------------------------------------------
# Employee
# --------------------------------------------------

employee_rows = []
employee_id = 1

employee_counts = {
    1: 22,
    2: 22,
    3: 18,
    4: 16,
    5: 16,
}

for store_id, count in employee_counts.items():

    for _ in range(count):

        employee_rows.append(
            [
                employee_id,
                store_id,
                random.randint(1, 8),
                f"Employee{employee_id}",
                f"Last{employee_id}",
                random.choice(
                    [
                        "Associate",
                        "Cashier",
                        "Stock Associate",
                        "Supervisor",
                    ]
                ),
                "2023-01-01",
                round(random.uniform(18, 34), 2),
                "Active",
            ]
        )

        employee_id += 1

employee_df = save_csv(
    "employee",
    employee_rows,
    [
        "employee_id",
        "store_id",
        "department_id",
        "first_name",
        "last_name",
        "job_title",
        "hire_date",
        "hourly_rate",
        "employment_status",
    ],
)


# --------------------------------------------------
# Employee Schedule
# --------------------------------------------------

schedule_rows = []
schedule_id = 1

start_date = datetime(2026, 7, 1)

for employee in employee_df.itertuples():

    for day_offset in range(7):

        schedule_rows.append(
            [
                schedule_id,
                employee.employee_id,
                (
                    start_date
                    + timedelta(days=day_offset)
                ).date(),
                "09:00",
                "17:00",
                round(
                    random.choice(
                        [0, 0, 0, 0, 1, 2]
                    ),
                    2,
                ),
                "Scheduled",
            ]
        )

        schedule_id += 1

schedule_df = save_csv(
    "employee_schedule",
    schedule_rows,
    [
        "schedule_id",
        "employee_id",
        "shift_date",
        "start_time",
        "end_time",
        "overtime_hours",
        "schedule_status",
    ],
)


# --------------------------------------------------
# Product
# --------------------------------------------------

base_products = [
    ("Organic Bananas", 1),
    ("Honeycrisp Apples", 1),
    ("Whole Milk", 2),
    ("Greek Yogurt", 2),
    ("Large Eggs", 2),
    ("Sourdough Bread", 3),
    ("Bagels", 3),
    ("Chicken Breast", 4),
    ("Ground Beef", 4),
    ("Frozen Pizza", 5),
    ("Ice Cream", 5),
    ("Orange Juice", 6),
    ("Sparkling Water", 6),
    ("Potato Chips", 7),
    ("Chocolate Cookies", 7),
    ("Paper Towels", 8),
    ("Dish Soap", 8),
    ("Toothpaste", 9),
    ("Shampoo", 9),
    ("Long Grain Rice", 10),
    ("Pasta", 10),
    ("Coffee", 10),
]

product_rows = []

for product_id in range(1, 251):

    base_name, category_id = base_products[
        (product_id - 1) % len(base_products)
    ]

    product_rows.append(
        [
            product_id,
            category_id,
            f"{base_name} {product_id}",
            f"Brand {(product_id % 15) + 1}",
            "1 unit",
            round(random.uniform(2.00, 25.00), 2),
            False,
        ]
    )

product_df = save_csv(
    "product",
    product_rows,
    [
        "product_id",
        "category_id",
        "product_name",
        "brand",
        "unit_size",
        "selling_price",
        "discontinued_status",
    ],
)


# --------------------------------------------------
# Store Inventory
# --------------------------------------------------

inventory_rows = []
inventory_id = 1

for store_id in range(1, 6):

    for product_id in range(1, 251):

        quantity = random.randint(40, 180)

        if (
            product_id % 17 == 0
            or random.random() < 0.04
        ):
            quantity = random.randint(2, 15)

        inventory_rows.append(
            [
                inventory_id,
                store_id,
                product_id,
                quantity,
                20,
                f"A{random.randint(1, 8)}",
                str(random.randint(1, 5)),
                "2026-08-01 08:00:00",
            ]
        )

        inventory_id += 1

inventory_df = save_csv(
    "store_inventory",
    inventory_rows,
    [
        "inventory_id",
        "store_id",
        "product_id",
        "quantity_on_hand",
        "reorder_level",
        "aisle_number",
        "shelf_number",
        "last_updated",
    ],
)


# --------------------------------------------------
# Inventory Adjustment
# --------------------------------------------------

adjustment_rows = []

for adjustment_id in range(1, 351):

    store_id = random.randint(1, 5)

    adjustment_rows.append(
        [
            adjustment_id,
            store_id,
            random.randint(1, 250),
            employee_for_store(
                employee_df,
                store_id,
            ),
            "2026-07-15 14:00:00",
            random.choice(
                [
                    "Damage",
                    "Spoilage",
                    "Correction",
                ]
            ),
            -random.randint(1, 5),
            "Inventory review",
        ]
    )

adjustment_df = save_csv(
    "inventory_adjustment",
    adjustment_rows,
    [
        "adjustment_id",
        "store_id",
        "product_id",
        "employee_id",
        "adjustment_date",
        "adjustment_type",
        "quantity_adjusted",
        "adjustment_notes",
    ],
)


# --------------------------------------------------
# Vendor Product
# --------------------------------------------------

vendor_product_rows = []

for product_id in range(1, 251):

    vendor_id = ((product_id - 1) % 10) + 1

    selling_price = float(
        product_df.loc[
            product_df["product_id"]
            == product_id,
            "selling_price",
        ].iloc[0]
    )

    vendor_product_rows.append(
        [
            product_id,
            vendor_id,
            product_id,
            round(
                selling_price
                * random.uniform(0.45, 0.7),
                2,
            ),
            random.choice([5, 10, 12]),
            random.randint(2, 7),
            product_id % 5 == 0,
        ]
    )

vendor_product_df = save_csv(
    "vendor_product",
    vendor_product_rows,
    [
        "vendor_product_id",
        "vendor_id",
        "product_id",
        "vendor_price",
        "minimum_order_quantity",
        "estimated_delivery_days",
        "is_preferred",
    ],
)


# --------------------------------------------------
# Purchase Order
# --------------------------------------------------

purchase_order_rows = []

for purchase_order_id in range(1, 201):

    store_id = weighted_store()

    purchase_order_rows.append(
        [
            purchase_order_id,
            random.randint(1, 10),
            store_id,
            employee_for_store(
                employee_df,
                store_id,
            ),
            "2026-06-01",
            "2026-06-05",
            "Received",
        ]
    )

purchase_order_df = save_csv(
    "purchase_order",
    purchase_order_rows,
    [
        "purchase_order_id",
        "vendor_id",
        "store_id",
        "employee_id",
        "order_date",
        "expected_delivery_date",
        "order_status",
    ],
)


# --------------------------------------------------
# Purchase Order Item
# --------------------------------------------------

purchase_order_item_rows = []
purchase_order_item_id = 1

for purchase_order_id in range(1, 201):

    # unique product IDs within the purchase order
    chosen_products = random.sample(
        range(1, 251),
        5,
    )

    for product_id in chosen_products:

        vendor_price = float(
            vendor_product_df.loc[
                vendor_product_df["product_id"]
                == product_id,
                "vendor_price",
            ].iloc[0]
        )

        quantity_ordered = random.randint(
            10,
            60,
        )

        purchase_order_item_rows.append(
            [
                purchase_order_item_id,
                purchase_order_id,
                product_id,
                quantity_ordered,
                vendor_price,
                quantity_ordered,
            ]
        )

        purchase_order_item_id += 1

purchase_order_item_df = save_csv(
    "purchase_order_item",
    purchase_order_item_rows,
    [
        "purchase_order_item_id",
        "purchase_order_id",
        "product_id",
        "quantity_ordered",
        "unit_cost",
        "quantity_received",
    ],
)


# --------------------------------------------------
# Delivery
# --------------------------------------------------

delivery_rows = []

for po in purchase_order_df.itertuples():

    vendor_id = po.vendor_id

    if vendor_id == 3:
        delay_days = random.choices(
            [2, 3, 4],
            weights=[40, 40, 20],
            k=1,
        )[0]
    else:
        delay_days = random.choices(
            [0, 1, 2, 3],
            weights=[55, 25, 15, 5],
            k=1,
        )[0]

    expected = datetime.strptime(
        po.expected_delivery_date,
        "%Y-%m-%d",
    )

    actual = (
        expected
        + timedelta(days=delay_days)
    )

    delivery_rows.append(
        [
            po.purchase_order_id,
            po.purchase_order_id,
            po.employee_id,
            actual.strftime(
                "%Y-%m-%d 10:00:00"
            ),
            "Delivered",
            (
                "Late delivery"
                if delay_days > 0
                else "On time"
            ),
        ]
    )

delivery_df = save_csv(
    "delivery",
    delivery_rows,
    [
        "delivery_id",
        "purchase_order_id",
        "received_by_employee_id",
        "actual_delivery_date",
        "delivery_status",
        "delivery_notes",
    ],
)


# --------------------------------------------------
# Sale
# --------------------------------------------------

sale_rows = []

monthly_weights = {
    1: 8,
    2: 10,
    3: 12,
    4: 14,
    5: 17,
    6: 19,
    7: 24,
}

months = list(
    monthly_weights.keys()
)

month_weights = list(
    monthly_weights.values()
)

for sale_id in range(1, 7001):

    store_id = weighted_store()

    month = random.choices(
        months,
        weights=month_weights,
        k=1,
    )[0]

    day = random.randint(1, 28)

    hour = random.choices(
        [9, 11, 13, 15, 17, 19],
        weights=[8, 12, 18, 16, 25, 21],
        k=1,
    )[0]

    sale_rows.append(
        [
            sale_id,
            store_id,
            random.randint(1, 700),
            employee_for_store(
                employee_df,
                store_id,
            ),
            (
                f"2026-{month:02d}-"
                f"{day:02d} "
                f"{hour:02d}:00:00"
            ),
            random.choice(
                [
                    "Credit",
                    "Debit",
                    "Cash",
                ]
            ),
        ]
    )

sale_df = save_csv(
    "sale",
    sale_rows,
    [
        "sale_id",
        "store_id",
        "customer_id",
        "employee_id",
        "sale_datetime",
        "payment_method",
    ],
)


# --------------------------------------------------
# Sale Item
# --------------------------------------------------

sale_item_rows = []
sale_item_id = 1

popular_products = list(
    range(1, 41)
)

all_products = list(
    range(1, 251)
)

for sale in sale_df.itertuples():

    item_count = random.randint(
        2,
        6,
    )

    selected = set()

    while len(selected) < item_count:

        if random.random() < 0.60:
            product_id = random.choice(
                popular_products
            )
        else:
            product_id = random.choice(
                all_products
            )

        selected.add(product_id)

    for product_id in selected:

        selling_price = float(
            product_df.loc[
                product_df["product_id"]
                == product_id,
                "selling_price",
            ].iloc[0]
        )

        max_qty = (
            4
            if sale.store_id == 5
            else 3
        )

        quantity = random.randint(
            1,
            max_qty,
        )

        discount = (
            round(
                selling_price * 0.10,
                2,
            )
            if random.random() < 0.10
            else 0.00
        )

        sale_item_rows.append(
            [
                sale_item_id,
                sale.sale_id,
                product_id,
                quantity,
                selling_price,
                discount,
            ]
        )

        sale_item_id += 1

sale_item_df = save_csv(
    "sale_item",
    sale_item_rows,
    [
        "sale_item_id",
        "sale_id",
        "product_id",
        "quantity",
        "unit_price",
        "discount_amount",
    ],
)


# --------------------------------------------------
# Store Expense
# --------------------------------------------------

store_expense_rows = []
expense_id = 1

monthly_store_expenses = {
    1: {
        "Rent": 12000,
        "Utilities": 3200,
        "Payroll": 23000,
    },
    2: {
        "Rent": 14500,
        "Utilities": 3800,
        "Payroll": 26000,
    },
    3: {
        "Rent": 9500,
        "Utilities": 2800,
        "Payroll": 19000,
    },
    4: {
        "Rent": 17000,
        "Utilities": 3000,
        "Payroll": 18000,
    },
    5: {
        "Rent": 19000,
        "Utilities": 2900,
        "Payroll": 17500,
    },
}

for month in range(1, 8):

    for store_id in range(1, 6):

        for expense_type, base_amount in (
            monthly_store_expenses[
                store_id
            ].items()
        ):

            store_expense_rows.append(
                [
                    expense_id,
                    store_id,
                    f"2026-{month:02d}-01",
                    expense_type,
                    f"{expense_type} expense",
                    round(
                        base_amount
                        * random.uniform(
                            0.95,
                            1.05,
                        ),
                        2,
                    ),
                ]
            )

            expense_id += 1

        store_expense_rows.append(
            [
                expense_id,
                store_id,
                f"2026-{month:02d}-15",
                "Maintenance",
                "Routine maintenance",
                round(
                    random.uniform(
                        500,
                        1800,
                    ),
                    2,
                ),
            ]
        )

        expense_id += 1

store_expense_df = save_csv(
    "store_expense",
    store_expense_rows,
    [
        "expense_id",
        "store_id",
        "expense_date",
        "expense_type",
        "description",
        "amount",
    ],
)


# --------------------------------------------------
# Final summary
# --------------------------------------------------

print()
print("=" * 60)
print("ABC FOODMART DATA GENERATED")
print("=" * 60)

for file in sorted(
    DATA_FOLDER.glob("*.csv")
):
    df = pd.read_csv(file)
    print(
        f"{file.name:<30}"
        f"{len(df):>8} rows"
    )

print()
print(
    f"Files saved to: {DATA_FOLDER}"
)