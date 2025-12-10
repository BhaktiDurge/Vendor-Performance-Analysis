USE vendor_performance;

-- 1st summary table
CREATE TABLE PurchaseSummary AS
SELECT
    p.VendorNo AS VendorNumber,
    p.VendorName,
    p.Brand,
    p.Description,
    p.PurchasePrice,
    pp.Price AS ActualPrice,
    pp.Volume,
    SUM(p.Quantity) AS TotalPurchaseQuantity,
    SUM(p.Dollars) AS TotalPurchaseDollars
FROM purchase p
JOIN purchase_price pp
    ON p.Brand = pp.Brand
WHERE p.PurchasePrice > 0
GROUP BY
    p.VendorNo,
    p.VendorName,
    p.Brand,
    p.Description,
    p.PurchasePrice,
    pp.Price,
    pp.Volume;
    
    
    -- 2nd summary table    
CREATE TABLE FreightSummary AS
SELECT
    VendorNo AS VendorNumber,
    SUM(Freight) AS FreightCost
FROM vendor_invoice
GROUP BY VendorNo;

-- creating a column row_id to so we can transfer data into chunks
ALTER TABLE sales_data
ADD COLUMN row_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
ADD PRIMARY KEY (row_id);


-- 3rd summary table first created a table then will load data into chunks cause huge amount of data is present in sala_data table
CREATE TABLE SalesSummary (
    VendorNo INT,
    Brand VARCHAR(255),
    TotalSalesQuantity DECIMAL(20,5),
    TotalSalesDollars DECIMAL(20,5),
    TotalSalesPrice DECIMAL(20,5),
    TotalExciseTax DECIMAL(20,5)
);

-- insertion of data into summary table
-- 1st chunk
INSERT INTO SalesSummary
SELECT VendorNo, Brand,
       SUM(SalesQuantity),
       SUM(SalesDollars),
       SUM(SalesPrice),
       SUM(ExciseTax)
FROM sales_data
WHERE row_id BETWEEN 1 AND 1000000
GROUP BY VendorNo, Brand;

-- 2nd chunk and so on...
INSERT INTO SalesSummary
SELECT VendorNo, Brand,
       SUM(SalesQuantity),
       SUM(SalesDollars),
       SUM(SalesPrice),
       SUM(ExciseTax)
FROM sales_data
WHERE row_id BETWEEN 1000001 AND 2000000
GROUP BY VendorNo, Brand;

-- last chunk
INSERT INTO SalesSummary
SELECT VendorNo, Brand,
       SUM(SalesQuantity),
       SUM(SalesDollars),
       SUM(SalesPrice),
       SUM(ExciseTax)
FROM sales_data
WHERE row_id BETWEEN 25000001 AND 25650727
GROUP BY VendorNo, Brand;










