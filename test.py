import mysql.connector

try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Megha@1995",
        database="food_db",
        auth_plugin='mysql_native_password'
    )
    print("✅ Connected successfully!")
except mysql.connector.Error as err:
    print("⚠️ Error:", err)
