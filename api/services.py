import os
import sqlite3

DB_PATH = os.path.join("data", "player_analysis.db")


def fetch_all(query, params=()):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    rows = conn.execute(query, params).fetchall()
    conn.close()

    return [dict(row) for row in rows]


def search_player_by_name(name):
    return fetch_all(
        """
        SELECT 
            s.*,
            COALESCE(v.market_value_text, 'N/a') AS market_value
        FROM fbref_player_stats s
        LEFT JOIN player_values v
            ON LOWER(s.player) = LOWER(v.player)
        WHERE LOWER(s.player) LIKE LOWER(?)
        ORDER BY s.team, s.player
        """,
        (f"%{name}%",),
    )


def search_players_by_club(club):
    return fetch_all(
        """
        SELECT 
            s.*,
            COALESCE(v.market_value_text, 'N/a') AS market_value
        FROM fbref_player_stats s
        LEFT JOIN player_values v
            ON LOWER(s.player) = LOWER(v.player)
        WHERE LOWER(s.team) LIKE LOWER(?)
        ORDER BY s.team, s.player
        """,
        (f"%{club}%",),
    )