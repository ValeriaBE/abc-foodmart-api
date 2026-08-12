-- Project Checkpoint 3
-- Group 1 SQL Code

-- 1. store
create table store (
    store_id serial primary key,
    store_name varchar(100) not null,
    street_address varchar(150) not null,
    city varchar(75) not null,
    state char(2) not null,
    zip_code varchar(10) not null,
    phone varchar(20),
    opening_date date,
    operating_status varchar(20) not null
);

-- 2. department
create table department (
    department_id serial primary key,
    department_name varchar(75) not null unique,
    description varchar(255)
);

-- 3. product_category
create table product_category (
    category_id serial primary key,
    category_name varchar(75) not null unique,
    category_description varchar(255)
);

-- 4. vendor
create table vendor (
    vendor_id serial primary key,
    vendor_name varchar(125) not null,
    contact_name varchar(100),
    phone varchar(20),
    email varchar(125),
    street_address varchar(150),
    city varchar(75),
    state char(2),
    zip_code varchar(10),
    vendor_status varchar(20) not null
);

-- 5. customer
create table customer (
    customer_id serial primary key,
    first_name varchar(50) not null,
    last_name varchar(50) not null,
    email varchar(125) unique,
    phone varchar(20),
    loyalty_join_date date,
    loyalty_points int default 0,
    membership_status varchar(20) not null
);

-- 6. employee
create table employee (
    employee_id serial primary key,
    store_id int not null,
    department_id int not null,
    first_name varchar(50) not null,
    last_name varchar(50) not null,
    job_title varchar(75) not null,
    hire_date date not null,
    hourly_rate decimal(8,2) not null,
    employment_status varchar(20) not null,
    constraint employee_store_fk foreign key (store_id) references store(store_id),
    constraint employee_department_fk foreign key (department_id) references department(department_id)
);

-- 7. employee_schedule
create table employee_schedule (
    schedule_id serial primary key,
    employee_id int not null,
    shift_date date not null,
    start_time time not null,
    end_time time not null,
    overtime_hours decimal(5,2) default 0.00,
    schedule_status varchar(20) not null,
    constraint schedule_employee_fk foreign key (employee_id) references employee(employee_id)
);

-- 8. product
create table product (
    product_id serial primary key,
    category_id int not null,
    product_name varchar(125) not null,
    brand varchar(75),
    unit_size varchar(30) not null,
    selling_price decimal(10,2) not null,
    discontinued_status boolean default false,
    constraint product_category_fk foreign key (category_id) references product_category(category_id)
);

-- 9. store_inventory
create table store_inventory (
    inventory_id serial primary key,
    store_id int not null,
    product_id int not null,
    quantity_on_hand int not null default 0,
    reorder_level int not null,
    aisle_number varchar(10),
    shelf_number varchar(10),
    last_updated timestamp not null,
    constraint inventory_store_fk foreign key (store_id) references store(store_id),
    constraint inventory_product_fk foreign key (product_id) references product(product_id),
    constraint store_product_uq unique (store_id, product_id)
);

-- 10. inventory_adjustment
create table inventory_adjustment (
    adjustment_id serial primary key,
    store_id int not null,
    product_id int not null,
    employee_id int not null,
    adjustment_date timestamp not null,
    adjustment_type varchar(30) not null,
    quantity_adjusted int not null,
    adjustment_notes varchar(255),
    constraint adj_store_fk foreign key (store_id) references store(store_id),
    constraint adj_product_fk foreign key (product_id) references product(product_id),
    constraint adj_employee_fk foreign key (employee_id) references employee(employee_id)
);

-- 11. vendor_product
create table vendor_product (
    vendor_product_id serial primary key,
    vendor_id int not null,
    product_id int not null,
    vendor_price decimal(10,2) not null,
    minimum_order_quantity int default 1,
    estimated_delivery_days int,
    is_preferred boolean default false,
    constraint vendor_product_vendor_fk foreign key (vendor_id) references vendor(vendor_id),
    constraint vendor_product_product_fk foreign key (product_id) references product(product_id),
    constraint vendor_product_uq unique (vendor_id, product_id)
);

-- 12. purchase_order
create table purchase_order (
    purchase_order_id serial primary key,
    vendor_id int not null,
    store_id int not null,
    employee_id int not null,
    order_date date not null,
    expected_delivery_date date,
    order_status varchar(25) not null,
    constraint po_vendor_fk foreign key (vendor_id) references vendor(vendor_id),
    constraint po_store_fk foreign key (store_id) references store(store_id),
    constraint po_employee_fk foreign key (employee_id) references employee(employee_id)
);

-- 13. purchase_order_item
create table purchase_order_item (
    purchase_order_item_id serial primary key,
    purchase_order_id int not null,
    product_id int not null,
    quantity_ordered int not null,
    unit_cost decimal(10,2) not null,
    quantity_received int default 0,
    constraint poi_purchase_order_fk foreign key (purchase_order_id) references purchase_order(purchase_order_id),
    constraint poi_product_fk foreign key (product_id) references product(product_id),
    constraint po_product_uq unique (purchase_order_id, product_id)
);

-- 14. delivery
create table delivery (
    delivery_id serial primary key,
    purchase_order_id int not null,
    received_by_employee_id int not null,
    actual_delivery_date timestamp,
    delivery_status varchar(25) not null,
    delivery_notes varchar(255),
    constraint delivery_po_fk foreign key (purchase_order_id) references purchase_order(purchase_order_id),
    constraint delivery_employee_fk foreign key (received_by_employee_id) references employee(employee_id)
);

-- 15. sale
create table sale (
    sale_id serial primary key,
    store_id int not null,
    customer_id int null,
    employee_id int not null,
    sale_datetime timestamp not null,
    payment_method varchar(25) not null,
    constraint sale_store_fk foreign key (store_id) references store(store_id),
    constraint sale_customer_fk foreign key (customer_id) references customer(customer_id),
    constraint sale_employee_fk foreign key (employee_id) references employee(employee_id)
);

-- 16. sale_item
create table sale_item (
    sale_item_id serial primary key,
    sale_id int not null,
    product_id int not null,
    quantity int not null,
    unit_price decimal(10,2) not null,
    discount_amount decimal(10,2) default 0.00,
    constraint sale_item_sale_fk foreign key (sale_id) references sale(sale_id),
    constraint sale_item_product_fk foreign key (product_id) references product(product_id)
);

-- 17. store_expense
create table store_expense (
    expense_id serial primary key,
    store_id int not null,
    expense_date date not null,
    expense_type varchar(50) not null,
    description varchar(255),
    amount decimal(12,2) not null,
    constraint expense_store_fk foreign key (store_id) references store(store_id)
);