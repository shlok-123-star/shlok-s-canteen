import sqlite3

def create_database():
    conn = sqlite3.connect("canteen.db")
    cursor = conn.cursor()

    # Old users table delete
    cursor.execute("DROP TABLE IF EXISTS users")

    # New users table
    cursor.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()
    print("Database created successfully!")