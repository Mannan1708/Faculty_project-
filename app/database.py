import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "faculty.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    # Enable WAL mode for high concurrency
    conn.execute('PRAGMA journal_mode=WAL')
    return conn
