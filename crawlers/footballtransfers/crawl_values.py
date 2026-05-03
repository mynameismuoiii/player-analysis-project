import re
import sqlite3
import time
from pathlib import Path

import pandas as pd
from bs4 import BeautifulSoup

from crawlers.footballtransfers.helpers import (
    build_search_url,
    clean_value_text,
    value_to_number,
)
from crawlers.footballtransfers.matcher import find_best_match
from crawlers.footballtransfers.retry import request_with_retry


ROOT_DIR = Path(__file__).resolve().parents[2]

FBREF_PLAYERS_CSV = ROOT_DIR / "data" / "processed" / "fbref_players_clean.csv"
OUTPUT_CSV = ROOT_DIR / "data" / "processed" / "player_values.csv"
DB_PATH = ROOT_DIR / "data" / "player_analysis.db"

TABLE_NAME = "player_values"


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}


def ensure_dirs():
    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)


def load_players() -> pd.DataFrame:
    if not FBREF_PLAYERS_CSV.exists():
        raise FileNotFoundError(
            f"Không thấy file {FBREF_PLAYERS_CSV}. "
            "Hãy chạy phần FBref trước."
        )

    df = pd.read_csv(FBREF_PLAYERS_CSV)

    required_cols = ["Player", "Squad"]

    for col in required_cols:
        if col not in df.columns:
            raise Exception(f"File FBref thiếu cột {col}")

    df = df[["Player", "Squad"]].drop_duplicates()

    return df


def parse_search_candidates(html: str) -> list[dict]:
    soup = BeautifulSoup(html, "html.parser")
    candidates = []

    text = soup.get_text(" ", strip=True)

    # Cách 1: thử lấy từ table nếu page có table
    for row in soup.select("tr"):
        row_text = row.get_text(" ", strip=True)

        if "€" not in row_text and "ETV" not in row_text:
            continue

        cols = [td.get_text(" ", strip=True) for td in row.select("td")]

        if not cols:
            continue

        value = extract_value_from_text(row_text)

        if value == "N/a":
            continue

        player_name = cols[0]

        candidates.append(
            {
                "player_name": player_name,
                "team": "N/a",
                "transfer_value": value,
                "transfer_value_number": value_to_number(value),
                "source": "footballtransfers",
            }
        )

    # Cách 2: fallback regex trên toàn trang
    if not candidates:
        value = extract_value_from_text(text)

        if value != "N/a":
            title = soup.find("h1")
            player_name = title.get_text(" ", strip=True) if title else "N/a"

            candidates.append(
                {
                    "player_name": player_name,
                    "team": "N/a",
                    "transfer_value": value,
                    "transfer_value_number": value_to_number(value),
                    "source": "footballtransfers",
                }
            )

    return candidates


def extract_value_from_text(text: str) -> str:
    if not text:
        return "N/a"

    patterns = [
        r"€\s?\d+(?:\.\d+)?\s?[mkMK]",
        r"£\s?\d+(?:\.\d+)?\s?[mkMK]",
        r"\$\s?\d+(?:\.\d+)?\s?[mkMK]",
    ]

    for pattern in patterns:
        match = re.search(pattern, text)

        if match:
            return clean_value_text(match.group(0).replace(" ", ""))

    return "N/a"


def crawl_one_player(player_name: str, squad: str) -> dict:
    url = build_search_url(player_name)

    try:
        html = request_with_retry(
            url=url,
            headers=HEADERS,
            max_retries=3,
            timeout=30,
            min_sleep=3,
            max_sleep=8,
        )

        candidates = parse_search_candidates(html)
        best = find_best_match(player_name, candidates)

        if best is None:
            return {
                "player_name": player_name,
                "squad": squad,
                "ft_player_name": "N/a",
                "transfer_value": "N/a",
                "transfer_value_number": None,
                "match_score": 0,
                "status": "NOT_FOUND",
                "source_url": url,
            }

        return {
            "player_name": player_name,
            "squad": squad,
            "ft_player_name": best.get("player_name", "N/a"),
            "transfer_value": best.get("transfer_value", "N/a"),
            "transfer_value_number": best.get("transfer_value_number"),
            "match_score": best.get("match_score", 0),
            "status": "FOUND",
            "source_url": url,
        }

    except Exception as e:
        print(f"Lỗi crawl {player_name}: {e}")

        return {
            "player_name": player_name,
            "squad": squad,
            "ft_player_name": "N/a",
            "transfer_value": "N/a",
            "transfer_value_number": None,
            "match_score": 0,
            "status": "ERROR",
            "source_url": url,
        }


def save_csv(df: pd.DataFrame):
    df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")
    print(f"Đã lưu CSV: {OUTPUT_CSV}")


def save_sqlite(df: pd.DataFrame):
    conn = sqlite3.connect(DB_PATH)

    df.to_sql(
        TABLE_NAME,
        conn,
        if_exists="replace",
        index=False,
    )

    conn.close()

    print(f"Đã lưu SQLite bảng {TABLE_NAME}: {DB_PATH}")


def crawl_values(limit: int | None = None) -> pd.DataFrame:
    ensure_dirs()

    players = load_players()

    if limit is not None:
        players = players.head(limit)

    results = []

    total = len(players)

    for index, row in players.iterrows():
        player_name = row["Player"]
        squad = row["Squad"]

        print(f"[{len(results) + 1}/{total}] Crawl value: {player_name} - {squad}")

        result = crawl_one_player(player_name, squad)
        results.append(result)

        time.sleep(5)

    df = pd.DataFrame(results)

    save_csv(df)
    save_sqlite(df)

    check_result(df)

    return df


def check_result(df: pd.DataFrame):
    print("\n========== CHECK PLAYER VALUES ==========")
    print("Shape:", df.shape)

    print("\nStatus count:")
    print(df["status"].value_counts())

    print("\nSample:")
    print(df.head(20))


if __name__ == "__main__":
    crawl_values()