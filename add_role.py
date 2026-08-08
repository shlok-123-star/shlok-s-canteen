import sqlite3

conn = sqlite3.connect("canteen.db")
cursor = conn.cursor()

cursor.execute("""
    ALTER TABLE users
    ADD COLUMN role TEXT DEFAULT 'student'
""")

conn.commit()
conn.close()

print("Role column added successfully!")