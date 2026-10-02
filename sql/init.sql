DROP TABLE IF EXISTS customers CASCADE;
DROP TABLE IF EXISTS products CASCADE;

CREATE TABLE customers (
    customer_id VARCHAR(10) PRIMARY KEY,
    join_date DATE NOT NULL,
    segment VARCHAR(50) NOT NULL
);

INSERT INTO customers (customer_id, join_date, segment)
SELECT
    'c' || lpad(i::text, 3, '0'),
    (CURRENT_DATE - (random() * 365)::int),
    (ARRAY['VIP', 'New', 'Regular', 'Lapsed'])[floor(random() * 4 + 1)]
FROM generate_series(1, 100) AS i;


CREATE TABLE products (
    product_id VARCHAR(10) PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    price NUMERIC(10, 2) NOT NULL CHECK (price > 0)
);

INSERT INTO products (product_id, product_name, category, price)
SELECT
    'p' || lpad(i::text, 3, '0'),
    'Product ' || (ARRAY['Alpha', 'Beta', 'Gamma', 'Delta', 'Omega'])[floor(random() * 5 + 1)] || ' ' || i,
    (ARRAY['Electronics', 'Books', 'Clothing', 'Home & Garden', 'Sports & Outdoors'])[floor(random() * 5 + 1)],
    round((random() * 490 + 10)::numeric, 2)
FROM generate_series(1, 50) AS i;
