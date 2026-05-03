import sqlite3
import time
from pathlib import Path

import pandas as pd
import requests

from crawlers.fbref.cleaning import clean_table, filter_minutes_over_90, final_clean
from crawlers.fbref.parser import get_player_table
from crawlers.fbref.selectors import FBREF_URLS, REQUEST_HEADERS


ROOT_DIR = Path(__file__).resolve().parents[2]

RAW_DIR = ROOT_DIR / "data" / "raw"
PROCESSED_DIR = ROOT_DIR / "data" / "processed"
DB_PATH = ROOT_DIR / "data" / "player_analysis.db"

RAW_CSV_PATH = RAW_DIR / "fbref_raw.csv"
PROCESSED_CSV_PATH = PROCESSED_DIR / "fbref_players_clean.csv"

TABLE_NAME = "player_stats"


def ensure_output_dirs() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def fetch_html(url: str) -> str:
    response = requests.get(
        url,
        headers=REQUEST_HEADERS,
        timeout=30,
    )

    response.raise_for_status()

    return response.text


def crawl_one_table(name: str, url: str) -> pd.DataFrame:
    print(f"Đang crawl bảng: {name}")

    html = fetch_html(url)
    df = get_player_table(html)
    df = clean_table(df, name)

    print(f"  -> {name}: {df.shape[0]} dòng, {df.shape[1]} cột")

    return df


def merge_tables(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    if "standard" not in tables:
        raise Exception("Thiếu bảng standard, không thể merge")

    base = tables["standard"]
    base = filter_minutes_over_90(base)

    for name, df in tables.items():
        if name == "standard":
            continue

        if "Player" not in df.columns or "Squad" not in df.columns:
            print(f"Bỏ qua bảng {name} vì thiếu Player hoặc Squad")
            continue

        df = df.drop(
            columns=["Nation", "Pos", "Age", "Born", "Comp"],
            errors="ignore",
        )

        base = base.merge(
            df,
            on=["Player", "Squad"],
            how="left",
        )

    base = base.loc[:, ~base.columns.duplicated()]
    base = final_clean(base)

    return base


def save_csv(df: pd.DataFrame, path: Path) -> None:
    df.to_csv(path, index=False, encoding="utf-8-sig")
    print(f"Đã lưu CSV: {path}")


def save_to_sqlite(df: pd.DataFrame) -> None:
    conn = sqlite3.connect(DB_PATH)

    df.to_sql(
        TABLE_NAME,
        conn,
        if_exists="replace",
        index=False,
    )

    conn.close()

    print(f"Đã lưu SQLite: {DB_PATH}")
    print(f"Bảng: {TABLE_NAME}")


def check_result(df: pd.DataFrame) -> None:
    print("\n========== CHECK RESULT ==========")
    print("Shape:", df.shape)

    print("\n5 dòng đầu:")
    print(df.head())

    print("\nCheck Min <= 90:")
    wrong_min = df[df["Min"] <= 90][["Player", "Squad", "Min"]]
    print(wrong_min)

    print("\nCheck trùng Player + Squad:")
    duplicated = df[df.duplicated(subset=["Player", "Squad"], keep=False)]
    print(duplicated[["Player", "Squad", "Min"]])

    print("\nSample Player, Squad, Min:")
    print(df[["Player", "Squad", "Min"]].head(20))


def crawl_fbref() -> pd.DataFrame:
    ensure_output_dirs()

    tables: dict[str, pd.DataFrame] = {}

    for name, url in FBREF_URLS.items():
        try:
            df = crawl_one_table(name, url)
            tables[name] = df

            # Tránh rate limit
            time.sleep(5)

        except Exception as e:
            print(f"Lỗi khi crawl bảng {name}: {e}")

    if "standard" not in tables:
        raise Exception("Không crawl được bảng standard")

    raw_df = tables["standard"]
    save_csv(raw_df, RAW_CSV_PATH)

    final_df = merge_tables(tables)

    save_csv(final_df, PROCESSED_CSV_PATH)
    save_to_sqlite(final_df)
    check_result(final_df)

    return final_df


if __name__ == "__main__":
    crawl_fbref()