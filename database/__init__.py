import os
import sqlite3

DB_PATH = os.path.join("data", "player_analysis.db")
SCHEMA_PATH = os.path.join("database", "schema.sql")


def init_db():
    os.makedirs("data", exist_ok=True)

    conn = sqlite3.connect(DB_PATH)

    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        conn.executescript(f.read())

    conn.commit()
    conn.close()

    print("Database initialized successfully.")


if __name__ == "__main__":
    init_db()