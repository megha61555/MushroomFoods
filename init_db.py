import sqlite3
import os

DB_FILE = 'mushroom.db'

# ---------- Remove old invalid database ----------
if os.path.exists(DB_FILE):
    try:
        # Try opening it to see if it's a valid SQLite DB
        conn = sqlite3.connect(DB_FILE)
        conn.execute("PRAGMA schema_version;")
        conn.close()
        print(f"✅ Existing database '{DB_FILE}' is valid, using it.")
    except sqlite3.DatabaseError:
        # Close connection if open
        try:
            conn.close()
        except:
            pass
        # Invalid database, remove it
        os.remove(DB_FILE)
        print(f"⚠ Existing file '{DB_FILE}' was not a valid database and has been removed.")
else:
    print(f"No existing database found. Creating '{DB_FILE}'.")

# ---------- Create new database ----------
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

# Enable foreign keys
cursor.execute("PRAGMA foreign_keys = ON;")

# ---------- Create Products Table ----------
cursor.execute('''
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT,
    description TEXT,
    price REAL,
    image_url TEXT,
    usage TEXT,
    health_benefits TEXT
)
''')

# ---------- Insert Sample Products ----------
sample_products = [
    ("Shiitake Mushroom", "Edible", "Rich in antioxidants and vitamins", 350, "static/images/garlic.jpg",
     "Cook in stir-fries or soups", "Boosts immunity and overall health"),
    ("Reishi Mushroom", "Medicinal", "Boosts immunity and reduces stress", 500, "static/images/peas.jpg",
     "Boil and drink as tea", "Reduces stress and improves sleep"),
    ("Oyster Mushroom", "Edible", "Low in calories, high in protein", 300, "static/images/sweetcorn.jpg",
     "Saute or grill", "Supports heart health")
]

cursor.executemany('''
INSERT INTO products (name, category, description, price, image_url, usage, health_benefits)
VALUES (?, ?, ?, ?, ?, ?, ?)
''', sample_products)

# ---------- Create Contacts Table ----------
cursor.execute('''
CREATE TABLE IF NOT EXISTS contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    message TEXT NOT NULL
)
''')

conn.commit()
conn.close()

print("✅ mushroom.db created successfully with tables and sample data!")
