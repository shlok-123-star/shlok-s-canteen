import sqlite3

conn = sqlite3.connect("canteen.db")
cursor = conn.cursor()

email = input("Enter your registered email: ")

cursor.execute(
    "UPDATE users SET role = 'admin' WHERE email = ?",
    (email,)
)

conn.commit()

if cursor.rowcount > 0:
    print("Admin role added successfully!")
else:
    print("Email not found!")

conn.close()