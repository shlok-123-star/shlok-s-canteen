import sqlite3

conn = sqlite3.connect("canteen.db")
cursor = conn.cursor()

cursor.execute("""
    ALTER TABLE orders
    ADD COLUMN status TEXT DEFAULT 'Pending'
""")

conn.commit()
conn.close()

print("Order status added successfully!")