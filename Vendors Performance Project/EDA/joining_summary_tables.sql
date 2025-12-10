use vendor_performance;

CREATE TABLE FinalSummary AS
SELECT
    ps.VendorNumber,
    ps.VendorName,
    ps.Brand,
    ps.Description,

    -- Purchase summary
    ps.TotalPurchaseQuantity,
    ps.TotalPurchaseDollars,
    ps.PurchasePrice,
    ps.ActualPrice,
    ps.Volume,

    -- Sales summary
    ss.TotalSalesQuantity,
    ss.TotalSalesDollars,
    ss.TotalSalesPrice,
    ss.TotalExciseTax,

    -- Freight summary
    fs.FreightCost

FROM PurchaseSummary ps
LEFT JOIN SalesSummary ss
       ON ps.VendorNumber = ss.VendorNo
      AND ps.Brand = ss.Brand
LEFT JOIN FreightSummary fs
       ON ps.VendorNumber = fs.VendorNumber;


-- -------------------------------------------------
-- 1. ADD 4 NEW COLUMNS (only if they don't exist)
-- -------------------------------------------------

ALTER TABLE FinalSummary
ADD COLUMN GrossProfit DECIMAL(20,5) NULL,
ADD COLUMN ProfitMargin DECIMAL(20,5) NULL,
ADD COLUMN StockTurnover DECIMAL(20,5) NULL,
ADD COLUMN SalesPurchaseRatio DECIMAL(20,5) NULL;

-- -------------------------------------------------
-- 2. UPDATE THE NEW COLUMNS WITH CALCULATED VALUES
-- -------------------------------------------------

UPDATE FinalSummary
SET GrossProfit = TotalSalesDollars - TotalPurchaseDollars;

UPDATE FinalSummary
SET ProfitMargin = 
    CASE 
        WHEN TotalSalesDollars = 0 THEN 0
        ELSE (GrossProfit / TotalSalesDollars) * 100
    END;

UPDATE FinalSummary
SET StockTurnover =
    CASE
        WHEN TotalPurchaseQuantity = 0 THEN 0
        ELSE TotalSalesQuantity / TotalPurchaseQuantity
    END;

UPDATE FinalSummary
SET SalesPurchaseRatio =
    CASE
        WHEN TotalPurchaseDollars = 0 THEN 0
        ELSE TotalSalesDollars / TotalPurchaseDollars
    END;

SHOW COLUMNS FROM FinalSummary;