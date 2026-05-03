import os
from database.db import get_connection

SCHEMA_PATH = os.path.join("database", "schema.sql")


def init_db():
    conn = get_connection()

    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        conn.executescript(f.read())

    conn.commit()
    conn.close()

    print("Database initialized successfully.")


if __name__ == "__main__":
    init_db()