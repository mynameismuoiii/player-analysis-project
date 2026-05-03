import os
import sqlite3

DB_PATH = os.path.join("data", "player_analysis.db")


def get_connection():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def fetch_all(query, params=()):
    conn = get_connection()
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def execute_query(query, params=()):
    conn = get_connection()
    cursor = conn.execute(query, params)
    conn.commit()
    conn.close()
    return cursor