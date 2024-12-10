import sqlite3

# connect to sqlite database
conn = sqlite3.connect("chat.db")

with sqlite3.connect('chat.db') as conn:
    cursor = conn.cursor()
    # create the messages tables
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS messages(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        content TEXT NOT NUll,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # create the users table if not exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
                )
    ''')

    conn.commit()

print("Data base initialized!")
