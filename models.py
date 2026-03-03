import sqlite3
def create_tables():
    conn = sqlite3.connect("smart_agent.db")
    cursor = conn.cursor()
    # Users Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)
    # Tasks Table
    cursor.execute("""CREATE TABLE IF NOT EXISTS tasks(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        task_text TEXT,
        status TEXT,
        priority TEXT,
        due_date TEXT,
        notification_time TEXT,
        notification_message TEXT
)
""")
    conn.commit()
    conn.close()
if __name__ == "__main__":
    create_tables()
