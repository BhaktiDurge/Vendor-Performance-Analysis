Use vendor_performance;

-- 1) Show all tables in the database
SHOW TABLES;

-- 2) Count number of records in each table
SELECT 'purchase' AS table_name, COUNT(*) AS total_rows FROM purchase;
SELECT 'purchase_price' AS table_name, COUNT(*) AS total_rows FROM purchase_price;
SELECT 'sales_data' AS table_name, COUNT(*) AS total_rows FROM sales_data;
SELECT 'begin_inventory' AS table_name, COUNT(*) AS total_rows FROM begin_inventory;
SELECT 'end_inventory' AS table_name, COUNT(*) AS total_rows FROM end_inventory;
SELECT 'vendor_invoice' AS table_name, COUNT(*) AS total_rows FROM vendor_invoice;
SELECT 'inventory_checkpoint' AS table_name, COUNT(*) AS total_rows FROM inventory_checkpoint;

-- 3) View first 5 rows of each table
SELECT * FROM purchase LIMIT 5;
SELECT * FROM purchase_price LIMIT 5;
SELECT * FROM sales_data LIMIT 5;
SELECT * FROM vendor_invoice LIMIT 5;
SELECT * FROM begin_inventory LIMIT 5;
SELECT * FROM end_inventory LIMIT 5;


-- EDA by vendor number from purchase table

SET @vno = 4466;

-- 5) Filter purchase table for that vendor @vno
SELECT * FROM purchase WHERE VendorNo = @vno ;
SELECT COUNT(*) AS filtered_purchase_rows 
FROM purchase 
WHERE VendorNo = @vno;

-- 6) Filter purchase_price table for that vendor @vno
SELECT * FROM purchase_price WHERE VendorNo = @vno ;
SELECT COUNT(*) AS filtered_purchase_rows 
FROM purchase_price
WHERE VendorNo = @vno;

-- 7) Filter sales_data table for that vendor @vno
SELECT * FROM sales_data WHERE VendorNo = @vno ;
SELECT COUNT(*) AS filtered_purchase_rows 
FROM sales_data
WHERE VendorNo = @vno;

-- 8) Group by analysis on Purchase table
SELECT 
    Brand,
    SUM(Quantity) AS total_quantity,
    SUM(Dollars) AS total_purchase_dollars
FROM purchase
GROUP BY Brand
ORDER BY total_purchase_dollars;


-- 9) Check if PO number is unique in vendor_invoice table
SELECT 
    PONumber,
    COUNT(*) AS count_po
FROM vendor_invoice
GROUP BY PONumber
HAVING COUNT(*) > 1;

ALTER TABLE sales_data 
ADD INDEX idx_brand (Brand);

-- Create a smaller table with 1–2 million rows
CREATE TABLE sales_data_sample AS
SELECT *
FROM sales_data
LIMIT 2000000;


SELECT Brand,
       SUM(SalesDollars),
       SUM(SalesPrice),
       SUM(SalesQuantity)
FROM sales_data_sample
GROUP BY Brand;

-- Conclusion :

-- The purchase table contains actual purchase data, include the date of purchase, product called brands, purchased by vendors, the amount paid in dollars, and the quantity purchased.
-- The PurchasePrice column is derived from the PurchasePrice table, which provide product-wise actual and purchase price.product-wise actual and purchase price.
-- The VendorInvoice table aggregates the data from the Purchase table, summarizing quantity and dollar amounts.
-- Along with an additional column for freight, this table maintains uniqueness based on vendors and plurals.
-- The Sales table captures actual sales transactions, detailing the brands purchased by vendors, the quantity sold, the selling price, and the revenue earned.
-- As the data that we need for analyze is distributed in different tables, we need to create a summarized table containing purchase transactions made by vendors, sales transactions data, freight cost for each vendors, actual product price for vendors.

