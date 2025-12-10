
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

from scipy.stats import ttest_ind
import scipy.stats as stats



import pandas as pd
df = pd.read_csv(r"C:\Users\Bhakti\OneDrive\Desktop\Documents\Vendors Performance Project\Cleaning_Analysis\filtered_finalsummary.csv")

'''

# 1] Identify brands that need promotional or pricing adjustments Low Sales Performance but High Profit Margin)
brand_performance = df.groupby('Description').agg({
    'TotalSalesDollars': 'sum',
    'ProfitMargin': 'mean'
}).reset_index()


#Threshold Calculation
low_sales_threshold = brand_performance['TotalSalesDollars'].quantile(0.15)
high_margin_threshold = brand_performance['ProfitMargin'].quantile(0.85)

print("Low Sales Threshold:", low_sales_threshold)
print("High Margin Threshold:", high_margin_threshold)


#Filter Target Brands
target_brands = brand_performance[
    (brand_performance['TotalSalesDollars'] <= low_sales_threshold) &
    (brand_performance['ProfitMargin'] >= high_margin_threshold)
]

print("\nBrands with LOW Sales but HIGH Profit Margin:")
print(target_brands.sort_values('TotalSalesDollars'))



# Visualization (Scatter Plot)
# limit for better visualization (optional)
filtered_performance = brand_performance[brand_performance['TotalSalesDollars'] < 10000]

plt.figure(figsize=(10, 6))

# All brands
sns.scatterplot(
    data=filtered_performance,
    x='TotalSalesDollars',
    y='ProfitMargin',
    label='All Brands',
    alpha=0.6
)

# Target brands
sns.scatterplot(
    data=target_brands,
    x='TotalSalesDollars',
    y='ProfitMargin',
    color='red',
    label='Target Brands'
)

# Threshold lines
plt.axvline(low_sales_threshold, color='black', linestyle='--', label='Low Sales Threshold')
plt.axhline(high_margin_threshold, color='black', linestyle='--', label='High Margin Threshold')

plt.xlabel("Total Sales ($)")
plt.ylabel("Profit Margin (%)")
plt.title("Brands for Promotional or Pricing Adjustments")
plt.legend()
plt.grid(True)
plt.show() 




# 2] Which vendors and brands demonstrate the highest sales performance?
# Function to format large numbers
def format_dollars(value):
    if value >= 1_000_000:
        return f"{value / 1_000_000:.2f}M"
    elif value >= 1_000:
        return f"{value / 1_000:.2f}K"
    else:
        return str(value)

# Top Vendors and Brands by Sales 
top_vendors = df.groupby("VendorName")["TotalSalesDollars"].sum().nlargest(10)
top_brands = df.groupby("Description")["TotalSalesDollars"].sum().nlargest(10)

print("\nTop 10 Vendors by Sales:")
print(top_vendors)

print("\nTop 10 Brands by Sales:")
print(top_brands)

# ============== Visualization ==============
plt.figure(figsize=(15, 8))

# Plot for Top Vendors
plt.subplot(1, 2, 1)
ax1 = sns.barplot(x=top_vendors.values, y=top_vendors.index, palette="Blues_r")
plt.title("Top 10 Vendors by Sales")
plt.xlabel("Total Sales ($)")
plt.ylabel("Vendor Name")

for bar in ax1.patches:
    ax1.text(
        bar.get_width() + (bar.get_width() * 0.01),
        bar.get_y() + bar.get_height() / 2,
        format_dollars(bar.get_width()),
        va="center", fontsize=9
    )

# Plot for Top Brands
plt.subplot(1, 2, 2)
ax2 = sns.barplot(x=top_brands.values, y=top_brands.index.astype(str), palette="Reds_r")
plt.title("Top 10 Brands by Sales")
plt.xlabel("Total Sales ($)")
plt.ylabel("Brand Name")

for bar in ax2.patches:
    ax2.text(
        bar.get_width() + (bar.get_width() * 0.01),
        bar.get_y() + bar.get_height() / 2,
        format_dollars(bar.get_width()),
        va="center", fontsize=9
    )

plt.tight_layout()
plt.show()



# 3]which vendor contribute the most to total purchase dollars
vendor_performance = df.groupby('VendorName').agg({
    'TotalPurchaseDollars': 'sum',
    'GrossProfit': 'sum',
    'TotalSalesDollars': 'sum'
}).reset_index()


# CONTRIBUTION PERCENTAGE
vendor_performance['PurchaseContribution%'] = (
    vendor_performance['TotalPurchaseDollars'] /
    vendor_performance['TotalPurchaseDollars'].sum()
) * 100

vendor_performance = vendor_performance.sort_values(
    'PurchaseContribution%', ascending=False
).round(2)

print(vendor_performance)


# TOP 10 VENDORS
top_vendors = vendor_performance.head(10).copy()

# Clean formatting
top_vendors['TotalPurchaseDollars'] = top_vendors['TotalPurchaseDollars'].apply(format_dollars)
top_vendors['GrossProfit'] = top_vendors['GrossProfit'].apply(format_dollars)
top_vendors['TotalSalesDollars'] = top_vendors['TotalSalesDollars'].apply(format_dollars)


# CUMULATIVE CONTRIBUTION
top_vendors['Cumulative_Contribution%'] = top_vendors['PurchaseContribution%'].cumsum()

print("\nTOP 10 VENDORS BY PURCHASE CONTRIBUTION:\n")
print(top_vendors)

# PARETO CHART
fig, ax1 = plt.subplots(figsize=(12, 6))

# Bar plot
sns.barplot(
    x=top_vendors['VendorName'],
    y=top_vendors['PurchaseContribution%'],
    palette="mako",
    ax=ax1
)

# Add labels on bars
for i, value in enumerate(top_vendors['PurchaseContribution%']):
    ax1.text(i, value + 0.5, f"{value}%", ha='center', fontsize=9, color='black')

# Line plot for cumulative %
ax2 = ax1.twinx()
ax2.plot(
    top_vendors['VendorName'],
    top_vendors['Cumulative_Contribution%'],
    color='red',
    marker='o',
    label="Cumulative Contribution %"
)

# Labels
ax1.set_xlabel("Vendor Name")
ax1.set_ylabel("Purchase Contribution %", color='blue')
ax2.set_ylabel("Cumulative Contribution %", color='red')
ax1.set_title("Pareto Chart: Vendor Contribution to Total Purchases")
plt.xticks(rotation=45, ha='right')

ax2.legend(loc='upper right')

plt.tight_layout()



#  4] how much of total procurement is depend onthe top vendors
# Calculate Total Contribution of Top Vendors
total_top10_contribution = top_vendors['PurchaseContribution%'].sum().round(2)

print(f"Total Purchase Contribution of Top 10 Vendors is {total_top10_contribution} %")

# Prepare data for Donut Chart
vendors = list(top_vendors['VendorName'].values)
purchase_contributions = list(top_vendors['PurchaseContribution%'].values)

# Remaining all vendors combined
remaining_contribution = 100 - total_top10_contribution

vendors.append("Other Vendors")
purchase_contributions.append(remaining_contribution)


# Donut Chart
fig, ax = plt.subplots(figsize=(8, 8))

wedges, texts, autotexts = ax.pie(
    purchase_contributions,
    labels=vendors,
    autopct='%1.1f%%',
    startangle=140,
    pctdistance=0.85
)

# Draw white circle in the center (donut effect)
centre_circle = plt.Circle((0, 0), 0.70, fc='white')
fig.gca().add_artist(centre_circle)

# Title
plt.title("Top 10 Vendors' Purchase Contribution (%)")
plt.show()



# 5] Does purchasing in bulk reduce the unit price and what is the optimal purchase volume for cost saving

df["UnitPurchasePrice"] = df["TotalPurchaseDollars"] / df["TotalPurchaseQuantity"]

# Create Order Size Categories (Small, Medium, Large)
df["OrderSize"] = pd.qcut(df["TotalPurchaseQuantity"], q=3, labels=["Small", "Medium", "Large"])

# Average Unit Price by Order Size
avg_unit_price = df.groupby("OrderSize")["UnitPurchasePrice"].mean()
print("\nAverage Unit Purchase Price by Order Size:\n")
print(avg_unit_price)

# Visualization: Boxplot
plt.figure(figsize=(10, 6))
sns.boxplot(data=df, x="OrderSize", y="UnitPurchasePrice", palette="Set2")
plt.title("Impact of Bulk Purchasing on Unit Price")
plt.xlabel("Order Size")
plt.ylabel("Unit Purchase Price")

plt.show()



low_turnover = (
    df[df["StockTurnover"] < 1]
    .groupby("VendorName")[["StockTurnover"]]
    .mean()
    .sort_values("StockTurnover", ascending=True)
    .head(10)     # Top 10 lowest turnover vendors
)

print("\nVendors with LOW Inventory Turnover (<1):\n")
print(low_turnover)



# 6] how much capital is locked in unsold inventory per vendor and which vendor contribute the most
df["UnsoldQuantity"] = (df["TotalPurchaseQuantity"] - df["TotalSalesQuantity"]).clip(lower=0)

df["UnsoldInventoryValue"] = df["UnsoldQuantity"] * df["PurchasePrice"]

print("Total Unsold Capital:", format_dollars(df["UnsoldInventoryValue"].sum()))

inventory_value_per_vendor = (
    df.groupby("VendorName")["UnsoldInventoryValue"]
      .sum()
      .reset_index()
)

inventory_value_per_vendor = inventory_value_per_vendor.sort_values(
    by="UnsoldInventoryValue", ascending=False
)

inventory_value_per_vendor['UnsoldInventoryValue'] = (
    inventory_value_per_vendor['UnsoldInventoryValue'].apply(format_dollars)
)

inventory_value_per_vendor.head(10)



# 7] Confidence Interval Comparison Top vs Low Vendors (Profit Margin)

vendor_margin = df.groupby("VendorName")["ProfitMargin"].mean()
vendor_margin_sorted = vendor_margin.sort_values(ascending=False)

# Thresholds (exact same as notebook)
top_threshold = int(len(vendor_margin_sorted) * 0.10)
low_threshold = int(len(vendor_margin_sorted) * 0.10)

# Select vendors
top_vendors_list = vendor_margin_sorted.head(top_threshold).index
low_vendors_list = vendor_margin_sorted.tail(low_threshold).index

# Extract profit margins
top_vendors = df[df["VendorName"].isin(top_vendors_list)]["ProfitMargin"]
low_vendors = df[df["VendorName"].isin(low_vendors_list)]["ProfitMargin"]

# Compute Mean & CI (Top Vendors)
top_mean = np.mean(top_vendors)
top_std = np.std(top_vendors, ddof=1)
top_n = len(top_vendors)
top_se = top_std / np.sqrt(top_n)
top_ci = stats.t.interval(0.95, df=top_n-1, loc=top_mean, scale=top_se)
top_lower, top_upper = top_ci

# Compute Mean & CI (Low Vendors)
low_mean = np.mean(low_vendors)
low_std = np.std(low_vendors, ddof=1)
low_n = len(low_vendors)
low_se = low_std / np.sqrt(low_n)
low_ci = stats.t.interval(0.95, df=low_n-1, loc=low_mean, scale=low_se)
low_lower, low_upper = low_ci

# ===========================
# PLOTTING STARTS (exact Jupyter code)
# ===========================

# Top Vendors Plot
sns.histplot(top_vendors, kde=True, color="blue", bins=30, alpha=0.5, label="Top Vendors")
plt.axvline(top_lower, color="blue", linestyle="--", label=f"Top Lower: {top_lower:.2f}")
plt.axvline(top_upper, color="blue", linestyle="--", label=f"Top Upper: {top_upper:.2f}")
plt.axvline(top_mean, color="blue", linestyle="--", label=f"Top Mean: {top_mean:.2f}")

# Low Vendors Plot
sns.histplot(low_vendors, kde=True, color="red", bins=30, alpha=0.5, label="Low Vendors")
plt.axvline(low_lower, color="red", linestyle="--", label=f"Low Lower: {low_lower:.2f}")
plt.axvline(low_upper, color="red", linestyle="--", label=f"Low Upper: {low_upper:.2f}")
plt.axvline(low_mean, color="red", linestyle="--", label=f"Low Mean: {low_mean:.2f}")

# Finalize Plot
plt.title("Confidence Interval Comparison: Top vs. Low Vendors (Profit Margin)")
plt.xlabel("Profit Margin (%)")
plt.ylabel("Frequency")
plt.legend()
plt.grid(True)
plt.show()'''


# 8] is there a singnificant difference between top-performing and low performing vendro
# Hypothesis:
# H₀ (Null Hypothesis): There is no significant difference in the mean profit margins of top-performing and low-performing vendors.
# H₁ (Alternative Hypothesis): The mean profit margins of top-performing and low-performing vendors are significantly different.

# Calculate thresholds
top_threshold = df["TotalSalesDollars"].quantile(0.75)
low_threshold = df["TotalSalesDollars"].quantile(0.25)

# Filter top and low vendors
top_vendors = df[df["TotalSalesDollars"] >= top_threshold]["ProfitMargin"].dropna()
low_vendors = df[df["TotalSalesDollars"] <= low_threshold]["ProfitMargin"].dropna()

# Perform Two-Sample T-Test
t_stat, p_value = ttest_ind(top_vendors, low_vendors, equal_var=False)

# Print results
print(f"T-Statistic: {t_stat:.4f}, P-Value: {p_value:.4f}")

if p_value < 0.05:
    print("Reject H₀: There is a significant difference in profit margins between top and low-performing vendors.")
else:
    print("Fail to Reject H₀: No significant difference in profit margins.")

# • The confidence interval for top-performing vendors (56.16% to 61.16%) 
#   is significantly higher than that of low-performing vendors (9.48% to 17.33%).

# • This indicates that vendors with higher sales also tend to maintain 
#   much higher profit margins.

# • For High-Performing Vendors: They can explore price optimization, 
#   bundling, or scaling strategies to further improve profitability.

# • For Low-Performing Vendors: Their very low margins suggest a need 
#   to review pricing, control costs, or improve product positioning.
