import sqlite3
from pathlib import Path


DB_PATH = "data/player_analysis.db"


def get_connection():
    Path("data").mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    return conn