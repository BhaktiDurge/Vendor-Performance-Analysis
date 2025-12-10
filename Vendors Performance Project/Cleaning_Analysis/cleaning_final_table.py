import pandas as pd
import mysql.connector as mysql

# -------------------------------------------------
# 1. CONNECT TO MYSQL
# -------------------------------------------------
connection = mysql.connect(
    host="localhost",
    user="root",
    password="Durge@123",
    database="vendor_performance"
)
print("✅ Connected to MySQL successfully!")

# -------------------------------------------------
# 2. LOAD THE FINAL SUMMARY TABLE (already updated)
# -------------------------------------------------
query = "SELECT * FROM FinalSummary;"
df = pd.read_sql(query, connection)

print("\n--- INFO BEFORE CLEANING ---")
print(df.info())
print("\nMissing values before cleaning:")
print(df.isnull().sum())

# -------------------------------------------------
# 3. CLEANING (light cleaning)
# -------------------------------------------------

# remove leading/trailing spaces
df["VendorName"] = df["VendorName"].astype(str).str.strip()
df["Description"] = df["Description"].astype(str).str.strip()

# fill missing numeric values with 0
df = df.fillna({
    "VendorName": "",
    "Description": "",
})
df = df.fillna(0)


print("\n--- INFO AFTER CLEANING ---")
print(df.info())

# -------------------------------------------------
# 4. PUSH CLEANED DATA BACK INTO MYSQL
# -------------------------------------------------
cursor = connection.cursor()

# truncate table to refill with cleaned values
cursor.execute("TRUNCATE TABLE FinalSummary")

# insert cleaned rows
cols = ", ".join(df.columns)
placeholders = ", ".join(["%s"] * len(df.columns))
insert_sql = f"INSERT INTO FinalSummary ({cols}) VALUES ({placeholders})"

for _, row in df.iterrows():
    cursor.execute(insert_sql, tuple(row))

connection.commit()
cursor.close()
connection.close()

print("\n✅ Cleaning completed & FinalSummary table updated successfully!")
