CREATE database vendor_performance;
USE vendor_performance;

CREATE TABLE purchase_price (
    Brand INT,
    Description VARCHAR(100),
    Price DECIMAL(10,2),
    Size VARCHAR(20),
    Volume INT,
    Classification INT,
    PurchasePrice DECIMAL(10,2),
    VendorNo INT,
    VendorName VARCHAR(100)
);

CREATE TABLE begin_inventory (
    InventoryId VARCHAR(50),
    Store INT,
    City VARCHAR(100),
    Brand INT,
    Description VARCHAR(100),
    Size VARCHAR(20),
    onHand INT,
    Price DECIMAL(10,2),
    startDate DATE
);



CREATE TABLE end_inventory (
    InventoryId VARCHAR(50),
    Store INT,
    City VARCHAR(100),
    Brand INT,
    Description VARCHAR(100),
    Size VARCHAR(20),
    onHand INT,
    Price DECIMAL(10,2),
    endDate DATE
);

CREATE TABLE purchase (
    InventoryId VARCHAR(50),
    Store INT,
    Brand INT,
    Description VARCHAR(100),
    Size VARCHAR(20),
    VendorNo INT,
    VendorName VARCHAR(100),
    PONumber INT,
    PODate DATE,
    ReceivingDate DATE,
    InvoiceDate DATE,
    PayDate DATE,
    PurchasePrice DECIMAL(10,2),
    Quantity INT,
    Dollars DECIMAL(12,2),
    Classification INT
);


CREATE TABLE sales_data (
    InventoryId VARCHAR(50),
    Store INT,
    Brand INT,
    Description VARCHAR(100),
    Size VARCHAR(20),
    SalesQuantity INT,
    SalesDollars DECIMAL(12,2),
    SalesPrice DECIMAL(10,2),
    SalesDate DATE,
    Volume INT,
    Classification INT,
    ExciseTax DECIMAL(10,2),
    VendorNo INT,
    VendorName VARCHAR(100)
);

CREATE TABLE vendor_invoice (
    VendorNo INT,
    VendorName VARCHAR(100),
    InvoiceDate DATE,
    PONumber INT,
    PODate DATE,
    PayDate DATE,
    Quantity INT,
    Dollars DECIMAL(12,2),
    Freight DECIMAL(10,2),
    Approval varchar(50)
);

CREATE TABLE inventory_checkpoint (
    InventoryId VARCHAR(50),
    Store INT,
    City VARCHAR(100),
    Brand INT,
    Description VARCHAR(100),
    Size VARCHAR(20),
    onHand INT,
    Price DECIMAL(10,2),
    startDate DATE
);

SET GLOBAL local_infile = 1;
SHOW VARIABLES LIKE 'local_infile';

LOAD DATA LOCAL INFILE 'C:/Users/Bhakti/Downloads/data/data/purchase_price.csv'
INTO TABLE purchase_price
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(Brand, Description, Price, Size, Volume, Classification, PurchasePrice, VendorNo, VendorName);

LOAD DATA LOCAL INFILE 'C:/Users/Bhakti/Downloads/data/data/begin_inventory.csv'
INTO TABLE begin_inventory
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(InventoryId, Store, City, Brand, Description, Size, onHand, Price, @startDate)
SET startDate = STR_TO_DATE(@startDate, '%Y-%m-%d');

LOAD DATA LOCAL INFILE 'C:/Users/Bhakti/Downloads/data/data/end_inventory.csv'
INTO TABLE end_inventory
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(InventoryId, Store, City, Brand, Description, Size, onHand, Price, @endDate)
SET endDate = STR_TO_DATE(@endDate, '%Y-%m-%d');


LOAD DATA LOCAL INFILE 'C:/Users/Bhakti/Downloads/data/data/purchase.csv'
INTO TABLE purchase
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(InventoryId, Store, Brand, Description, Size, VendorNo, VendorName, PONumber, @PODate, @ReceivingDate, @InvoiceDate, @PayDate, PurchasePrice, Quantity, Dollars, Classification)
SET 
  PODate = STR_TO_DATE(@PODate, '%Y-%m-%d'),
  ReceivingDate = STR_TO_DATE(@ReceivingDate, '%Y-%m-%d'),
  InvoiceDate = STR_TO_DATE(@InvoiceDate, '%Y-%m-%d'),
  PayDate = STR_TO_DATE(@PayDate, '%Y-%m-%d');
 
 LOAD DATA LOCAL INFILE 'C:/Users/Bhakti/Downloads/data/data/sales_data.csv'
INTO TABLE sales_data
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(InventoryId, Store, Brand, Description, Size, SalesQuantity, SalesDollars, SalesPrice, @SalesDate, Volume, Classification, ExciseTax, VendorNo, VendorName)
SET 
  SalesDate = STR_TO_DATE(@SalesDate, '%Y-%m-%d');


LOAD DATA LOCAL INFILE 'C:/Users/Bhakti/Downloads/data/data/vendor_invoice.csv'
INTO TABLE vendor_invoice
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(VendorNo, VendorName, @InvoiceDate, PONumber, @PODate, @PayDate, Quantity, Dollars, Freight, Approval)
SET
  InvoiceDate = STR_TO_DATE(@InvoiceDate, '%Y-%m-%d'),
  PODate = STR_TO_DATE(@PODate, '%Y-%m-%d'),
  PayDate = STR_TO_DATE(@PayDate, '%Y-%m-%d');
  
  
  LOAD DATA LOCAL INFILE 'C:/Users/Bhakti/Downloads/data/data/.ipynb_checkpoints/begin_inventory-checkpoint.csv'
INTO TABLE inventory_checkpoint
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(InventoryId, Store, City, Brand, Description, Size, onHand, Price, @startDate)
SET 
  startDate = STR_TO_DATE(@startDate, '%Y-%m-%d');

  
SELECT COUNT(*) FROM sales_data;
