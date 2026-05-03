import os
import sqlite3

DB_PATH = os.path.join("data", "player_analysis.db")


def fetch_all(query, params=()):
    if not os.path.exists(DB_PATH):
        raise FileNotFoundError(f"Không tìm thấy database: {DB_PATH}")

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    try:
        rows = conn.execute(query, params).fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()


def table_exists(table_name):
    result = fetch_all(
        """
        SELECT name
        FROM sqlite_master
        WHERE type = 'table' AND name = ?
        """,
        (table_name,),
    )
    return len(result) > 0


def get_columns(table_name):
    rows = fetch_all(f"PRAGMA table_info({table_name})")
    return [row["name"] for row in rows]


def get_team_column():
    columns = get_columns("fbref_player_stats")

    if "team" in columns:
        return "team"

    if "squad" in columns:
        return "squad"

    raise Exception("Không tìm thấy cột team hoặc squad trong bảng fbref_player_stats")


def has_player_values():
    if not table_exists("player_values"):
        return False

    columns = get_columns("player_values")
    return "player" in columns and "market_value_text" in columns


def search_player_by_name(name):
    team_col = get_team_column()

    if has_player_values():
        query = f"""
            SELECT 
                s.*,
                COALESCE(v.market_value_text, 'N/a') AS market_value
            FROM fbref_player_stats s
            LEFT JOIN player_values v
                ON LOWER(s.player) = LOWER(v.player)
            WHERE LOWER(s.player) LIKE LOWER(?)
            ORDER BY s.{team_col}, s.player
        """
    else:
        query = f"""
            SELECT 
                s.*,
                'N/a' AS market_value
            FROM fbref_player_stats s
            WHERE LOWER(s.player) LIKE LOWER(?)
            ORDER BY s.{team_col}, s.player
        """

    return fetch_all(query, (f"%{name}%",))


def search_players_by_club(club):
    team_col = get_team_column()

    if has_player_values():
        query = f"""
            SELECT 
                s.*,
                COALESCE(v.market_value_text, 'N/a') AS market_value
            FROM fbref_player_stats s
            LEFT JOIN player_values v
                ON LOWER(s.player) = LOWER(v.player)
            WHERE LOWER(s.{team_col}) LIKE LOWER(?)
            ORDER BY s.{team_col}, s.player
        """
    else:
        query = f"""
            SELECT 
                s.*,
                'N/a' AS market_value
            FROM fbref_player_stats s
            WHERE LOWER(s.{team_col}) LIKE LOWER(?)
            ORDER BY s.{team_col}, s.player
        """

    return fetch_all(query, (f"%{club}%",))