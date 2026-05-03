from pathlib import Path

from database.db import get_connection


SCHEMA_PATH = "database/schema.sql"


def init_database():
    Path("data").mkdir(parents=True, exist_ok=True)

    conn = get_connection()

    with open(SCHEMA_PATH, "r", encoding="utf-8") as file:
        schema = file.read()

    conn.executescript(schema)
    conn.commit()
    conn.close()

    print("DONE: Đã khởi tạo database")
    print("Database: data/player_analysis.db")


if __name__ == "__main__":
    init_database()