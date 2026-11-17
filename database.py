
import sqlite3

DB_NAME = "smartstudy.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def init_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                deadline TEXT NOT NULL,
                hours REAL NOT NULL,
                priority INTEGER NOT NULL,
                completed_hours REAL DEFAULT 0
            )
        """)


def add_task(name, deadline, hours, priority):
    with get_connection() as conn:
        conn.execute("""
            INSERT INTO tasks
            (name, deadline, hours, priority)
            VALUES (?, ?, ?, ?)
        """, (name, str(deadline), hours, priority))


def get_tasks():
    with get_connection() as conn:
        return conn.execute("""
            SELECT id, name, deadline, hours,
                   priority, completed_hours
            FROM tasks
            ORDER BY deadline ASC
        """).fetchall()


def delete_task(task_id):
    with get_connection() as conn:
        conn.execute(
            "DELETE FROM tasks WHERE id = ?",
            (task_id,)
        )
