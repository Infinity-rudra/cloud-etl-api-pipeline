-- ============================================================
-- ANALYTICS QUERIES
-- Source: analytics.products
-- ============================================================


-- 1. Total products
SELECT
    COUNT(*) AS total_products
FROM analytics.products;


-- 2. Category-wise product count and average price
SELECT
    category,
    COUNT(*) AS product_count,
    ROUND(AVG(price), 2) AS average_price
FROM analytics.products
GROUP BY category
ORDER BY product_count DESC;


-- 3. Total and average stock
SELECT
    SUM(stock) AS total_stock,
    ROUND(AVG(stock), 2) AS average_stock
FROM analytics.products;


-- 4. Top 10 most expensive products
SELECT
    id,
    title,
    category,
    price
FROM analytics.products
ORDER BY price DESC
LIMIT 10;


-- 5. Low-stock products
SELECT
    COUNT(*) AS low_stock_products
FROM analytics.products
WHERE stock < 20;


-- 6. Category-wise stock and price analysis
SELECT
    category,
    COUNT(*) AS product_count,
    SUM(stock) AS total_stock,
    ROUND(AVG(price), 2) AS average_price
FROM analytics.products
GROUP BY category
ORDER BY total_stock DESC;


-- 7. Category price range
SELECT
    category,
    MAX(price) AS highest_price,
    MIN(price) AS lowest_price,
    ROUND(AVG(price), 2) AS average_price
FROM analytics.products
GROUP BY category
ORDER BY highest_price DESC;


-- 8. Data quality check
SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT id) AS unique_ids
FROM analytics.products;


-- 9. Average rating by category
SELECT
    category,
    ROUND(AVG(rating), 2) AS average_rating
FROM analytics.products
GROUP BY category
ORDER BY average_rating DESC;


-- 10. Low-stock product details
SELECT
    id,
    title,
    category,
    stock,
    price
FROM analytics.products
WHERE stock < 20
ORDER BY stock ASC;


-- 11. Category inventory summary
SELECT
    category,
    COUNT(*) AS product_count,
    SUM(stock) AS total_stock,
    ROUND(AVG(stock), 2) AS average_stock
FROM analytics.products
GROUP BY category
ORDER BY total_stock DESC;


-- 12. Product price distribution
SELECT
    CASE
        WHEN price < 100 THEN '< $100'
        WHEN price < 500 THEN '$100 - $499'
        WHEN price < 1000 THEN '$500 - $999'
        ELSE '$1000+'
    END AS price_range,
    COUNT(*) AS product_count
FROM analytics.products
GROUP BY price_range
ORDER BY product_count DESC;