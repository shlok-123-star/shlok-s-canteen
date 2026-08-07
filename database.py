import sqlite3

conn = sqlite3.connect("canteen.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
)
""")

cursor.execute("""
INSERT OR IGNORE INTO users(username, password)
VALUES ('admin', '1234')
""")

cursor.execute("""
INSERT OR IGNORE INTO users(username, password)
VALUES ('student', '1111')
""")

conn.commit()
conn.close()

print("Database Created Successfully")