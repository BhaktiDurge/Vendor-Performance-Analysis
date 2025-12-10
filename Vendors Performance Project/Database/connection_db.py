import mysql.connector as mysql

connection = mysql.connect(
    host="localhost",
    user="root",
    password="Durge@123",
    database="vendor_performance"
)

if connection.is_connected():
    print("✅ Connected to MySQL successfully!")

