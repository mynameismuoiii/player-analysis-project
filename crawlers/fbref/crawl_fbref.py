import os
import sqlite3
import pandas as pd
import soccerdata as sd

from crawlers.fbref.selectors import (
    SOCCERDATA_LEAGUE,
    SOCCERDATA_SEASON,
    FBREF_STAT_TYPES,
    MERGE_KEYS,
)
from crawlers.fbref.parser import parse_soccerdata_table
from crawlers.fbref.cleaning import filter_players_over_90_minutes, make_sqlite_safe


DB_PATH = os.path.join("data", "player_analysis.db")
PROCESSED_DIR = os.path.join("data", "processed")


def create_fbref_client():
    return sd.FBref(
        leagues=SOCCERDATA_LEAGUE,
        seasons=SOCCERDATA_SEASON,
    )


def crawl_one_table(fbref, table_name: str, stat_type: str) -> pd.DataFrame:
    print(f"Đang lấy bảng {table_name} từ FBref bằng soccerdata...")

    df = fbref.read_player_season_stats(stat_type=stat_type)
    df = parse_soccerdata_table(df, table_name)

    print(f"Xong bảng {table_name}: {len(df)} dòng, {len(df.columns)} cột")

    return df


def merge_fbref_tables(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    standard_df = tables["standard"]
    standard_df = filter_players_over_90_minutes(standard_df)

    final_df = standard_df.copy()

    for table_name, df in tables.items():
        if table_name == "standard":
            continue

        available_keys = [
            key for key in MERGE_KEYS
            if key in final_df.columns and key in df.columns
        ]

        if not available_keys:
            print(f"Bỏ qua bảng {table_name} vì không có key chung.")
            continue

        final_df = final_df.merge(
            df,
            how="left",
            on=available_keys,
            suffixes=("", f"_{table_name}"),
        )

    final_df = final_df.fillna("N/a")
    final_df = make_sqlite_safe(final_df)

    return final_df


def save_to_sqlite(df: pd.DataFrame):
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    conn = sqlite3.connect(DB_PATH)

    df.to_sql(
        "fbref_player_stats",
        conn,
        if_exists="replace",
        index=False,
    )

    conn.close()

    print(f"Đã lưu bảng fbref_player_stats vào {DB_PATH}")


def save_to_csv(df: pd.DataFrame):
    os.makedirs(PROCESSED_DIR, exist_ok=True)

    path = os.path.join(PROCESSED_DIR, "fbref_player_stats.csv")
    df.to_csv(path, index=False, encoding="utf-8-sig")

    print(f"Đã xuất CSV: {path}")


def crawl_fbref_players():
    fbref = create_fbref_client()

    tables = {}

    for table_name, stat_type in FBREF_STAT_TYPES.items():
        try:
            tables[table_name] = crawl_one_table(fbref, table_name, stat_type)
        except Exception as e:
            print(f"Lỗi bảng {table_name}: {e}")

    if "standard" not in tables:
        raise Exception("Không lấy được bảng standard nên không thể tiếp tục.")

    final_df = merge_fbref_tables(tables)

    save_to_sqlite(final_df)
    save_to_csv(final_df)

    print("Hoàn thành crawl dữ liệu FBref.")

    return final_df


if __name__ == "__main__":
    crawl_fbref_players()