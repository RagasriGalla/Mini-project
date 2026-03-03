from datetime import datetime, timedelta
import sqlite3
def add_task(user_id, task_text, due_date, priority="medium"):
    conn = sqlite3.connect("smart_agent.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tasks(user_id, task_text, status, due_date)
        VALUES (?, ?, ?, ?)
    """, (user_id, task_text, "pending", due_date))
    conn.commit()
    conn.close()
def update_task_status(task_id, status):
    conn = sqlite3.connect("smart_agent.db")
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE tasks
        SET status = ?
        WHERE id = ?
    """, (status, task_id))
    conn.commit()
    conn.close()
def delete_task(task_id):
    conn = sqlite3.connect("smart_agent.db")
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM tasks
        WHERE id = ?
    """, (task_id,))
    conn.commit()
    conn.close()
def get_tasks():
    conn = sqlite3.connect("smart_agent.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    conn.close()
    return tasks
def reschedule_task(task_id):
    conn = sqlite3.connect("smart_agent.db")
    cursor = conn.cursor()
    # Move to next day 
    new_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    cursor.execute("""
        UPDATE tasks
        SET due_date = ?
        WHERE id = ?
    """, (new_date, task_id))
    conn.commit()
    conn.close()
    return new_date
