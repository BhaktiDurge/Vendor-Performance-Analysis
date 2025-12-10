import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import mysql.connector as mysql

warnings.filterwarnings('ignore')

connection = mysql.connect(
    host="localhost",
    user="root",
    password="Durge@123",
    database="vendor_performance"
)

if connection.is_connected():
    print("✅ Connected to MySQL successfully!")

    # loading table into datafram
    query = "SELECT * FROM FinalSummary;"
df = pd.read_sql(query, connection)


summary_satats = df.describe().T
print(summary_satats)


# Distribution Plot for nuercical columns
numerical_cols = df.select_dtypes(include=np.number).columns

plt.figure(figsize=(15, 10))
for i, col in enumerate(numerical_cols):
    plt.subplot(4, 4, i + 1)
    sns.histplot(df[col], kde=True, bins=30)
    plt.title(col)

plt.tight_layout()
plt.show()


 #Outlier Detection with BoxPlots
plt.figure(figsize=(15, 10))
for i, col in enumerate(numerical_cols):
    plt.subplot(4, 4, i + 1)
    sns.boxplot(y=df[col])
    plt.title(col)

plt.tight_layout()
plt.show()



# ============================================
# SUMMARY STATISTIC INSIGHTS
# ============================================

# 1. NEGATIVE AND ZERO VALUES
# --------------------------------------------
# • Gross Profit: Minimum value is -52,002.78, indicating losses.
#   This means some products or transactions may be selling at a loss
#   due to high costs or discounting below the purchase price.
#
# • Profit Margin: Minimum value is -∞ (negative infinity), which
#   suggests cases where revenue is zero or lower than the cost.
#   This typically happens when items are given away for free or returned.
#
# • Total Sales Quantity & Sales Dollar: Minimum values are zero,
#   meaning some products were purchased but never sold.
#   These could be slow-moving or obsolete stock items.

# 2. OUTLIERS INDICATED BY HIGH STANDARD DEVIATION
# ------------------------------------------------
# • Purchase Price & Actual Price:
#   Maximum values (5,681.81 and 7,499.99) are significantly higher
#   than the mean values (24.39 and 35.64), indicating premium or
#   high-value product categories.
#
# • Freight Cost:
#   Huge variation from 0.09 to 257,032.07 suggests logistical
#   inefficiencies, bulk shipments, or exceptional transportation charges.
#
# • Stock Turnover:
#   Ranges from 0 to 274.5, implying that some products sell extremely fast
#   while others remain in stock indefinitely.
#   Values greater than 1 indicate that the sold quantity for a product
#   exceeds the purchased quantity — possibly fulfilled using older stock.


 # Filter the data by removing inconsistencies
df = pd.read_sql_query("""
    SELECT *
    FROM FinalSummary
    WHERE GrossProfit > 0
      AND ProfitMargin > 0
      AND TotalSalesQuantity > 0
""", connection)

df.to_csv("filtered_finalsummary.csv", index=False)


# after filtering checking Distribution Plot for nuercical columns
numerical_cols = df.select_dtypes(include=np.number).columns

plt.figure(figsize=(15, 10))
for i, col in enumerate(numerical_cols):
    plt.subplot(4, 4, i + 1)
    sns.histplot(df[col], kde=True, bins=30)
    plt.title(col)

plt.tight_layout()
plt.show()

# Count Plot for categorical column
categorical_cols = ["VendorName", "Description"]

plt.figure(figsize=(12, 5))
for i, col in enumerate(categorical_cols):
    plt.subplot(1, 2, i + 1)
    sns.countplot(y=df[col], order=df[col].value_counts().index[:10])
    plt.title(f"Top 10 {col}")

plt.tight_layout()
plt.show()

# Correlation heatmap
plt.figure(figsize=(12, 8))
numerical_cols = df.select_dtypes(include=['int64', 'float64']).columns
correlation_matrix = df[numerical_cols].corr()
sns.heatmap(
    correlation_matrix,
    annot=True,
    fmt=".2f",
    cmap="coolwarm",
    linewidths=0.5
)

plt.title("Correlation Heatmap")
plt.show()


# STRONG POSITIVE RELATIONSHIPS
# --------------------------------------------
# • ActualPrice and PurchasePrice show an extremely strong correlation (~0.99),
#   indicating that selling price closely follows purchase cost.
#
# • TotalPurchaseDollars and TotalSalesDollars have a strong correlation (~0.92),
#   meaning higher purchase investment leads to higher sales revenue.
#
# • TotalPurchaseQuantity and TotalSalesQuantity are highly correlated (~0.82),
#   suggesting products purchased in larger quantities are also sold more.



