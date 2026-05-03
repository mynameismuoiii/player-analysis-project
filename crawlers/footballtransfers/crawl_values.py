import os
import re
import time
import sqlite3
from bs4 import BeautifulSoup

from crawlers.footballtransfers.helpers import build_search_url, market_value_to_number
from crawlers.footballtransfers.retry import get_with_retry

DB_PATH = os.path.join("data", "player_analysis.db")

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def create_player_values_table():
    conn = sqlite3.connect(DB_PATH)

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS player_values (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player TEXT NOT NULL,
            team TEXT,
            matched_name TEXT DEFAULT 'N/a',
            market_value_text TEXT DEFAULT 'N/a',
            market_value_eur REAL,
            source TEXT DEFAULT 'footballtransfers',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    conn.commit()
    conn.close()


def get_players_from_fbref():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    rows = conn.execute(
        """
        SELECT DISTINCT player, team
        FROM fbref_player_stats
        WHERE player IS NOT NULL
        ORDER BY team, player
        """
    ).fetchall()

    conn.close()

    return [dict(row) for row in rows]


def extract_market_value(html):
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(" ", strip=True)

    matches = re.findall(r"€\s?\d+(?:\.\d+)?\s?[mMkK]", text)

    if not matches:
        return "N/a"

    return matches[0].replace(" ", "")


def crawl_value_for_player(player_name):
    url = build_search_url(player_name)

    response = get_with_retry(
        url,
        headers=HEADERS,
        retries=3,
        sleep_seconds=3,
        timeout=20,
    )

    if response is None:
        return "N/a"

    return extract_market_value(response.text)


def clear_old_values():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("DELETE FROM player_values")
    conn.commit()
    conn.close()


def save_player_value(player, team, market_value_text):
    conn = sqlite3.connect(DB_PATH)

    conn.execute(
        """
        INSERT INTO player_values (
            player,
            team,
            matched_name,
            market_value_text,
            market_value_eur,
            source
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            player,
            team,
            player,
            market_value_text,
            market_value_to_number(market_value_text),
            "footballtransfers",
        ),
    )

    conn.commit()
    conn.close()


def crawl_all_values():
    create_player_values_table()

    players = get_players_from_fbref()

    if not players:
        print("Chưa có bảng fbref_player_stats hoặc bảng đang rỗng.")
        print("Chạy trước: python -m crawlers.fbref.crawl_fbref")
        return

    clear_old_values()

    print(f"Tìm thấy {len(players)} cầu thủ từ fbref_player_stats.")

    for index, row in enumerate(players, start=1):
        player = row["player"]
        team = row["team"]

        print(f"[{index}/{len(players)}] Crawl giá: {player} - {team}")

        market_value_text = crawl_value_for_player(player)

        save_player_value(
            player=player,
            team=team,
            market_value_text=market_value_text,
        )

        time.sleep(2)

    print("Hoàn thành crawl giá chuyển nhượng.")


if __name__ == "__main__":
    crawl_all_values()