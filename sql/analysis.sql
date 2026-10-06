-- 1. Total products
SELECT COUNT(*) AS total_products
FROM products;


-- 2. Category-wise product count and average price
SELECT
    category,
    COUNT(*) AS product_count,
    ROUND(AVG(price), 2) AS average_price
FROM products
GROUP BY category
ORDER BY product_count DESC;


-- 3. Total and average stock
SELECT
    SUM(stock) AS total_stock,
    ROUND(AVG(stock), 2) AS average_stock
FROM products;


-- 4. Top 10 most expensive products
SELECT
    id,
    title,
    category,
    price
FROM products
ORDER BY price DESC
LIMIT 10;


-- 5. Low-stock products
SELECT
    COUNT(*) AS low_stock_products
FROM products
WHERE stock < 20;


-- 6. Category-wise stock and price analysis
SELECT
    category,
    COUNT(*) AS product_count,
    SUM(stock) AS total_stock,
    ROUND(AVG(price), 2) AS average_price
FROM products
GROUP BY category
ORDER BY total_stock DESC;


-- 7. Category price range
SELECT
    category,
    MAX(price) AS highest_price,
    MIN(price) AS lowest_price,
    ROUND(AVG(price), 2) AS average_price
FROM products
GROUP BY category
ORDER BY highest_price DESC;


-- 8. Check duplicate IDs
SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT id) AS unique_ids
FROM products;