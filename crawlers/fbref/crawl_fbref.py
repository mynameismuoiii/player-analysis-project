import sqlite3
from pathlib import Path

from crawlers.fbref.selectors import (
    TABLE_ID,
    MIN_MINUTES,
    DB_PATH,
    TABLE_NAME,
    HTML_CACHE_PATH,
)

from crawlers.fbref.parser import (
    extract_table_html,
    parse_fbref_table,
)

from crawlers.fbref.cleaning import (
    clean_column_names,
    remove_repeated_headers,
    filter_minutes,
    clean_nan,
)


def save_to_sqlite(df):
    Path("data").mkdir(exist_ok=True)

    conn = sqlite3.connect(DB_PATH)

    df.to_sql(
        TABLE_NAME,
        conn,
        if_exists="replace",
        index=False,
    )

    conn.close()


def main():
    print("Đang đọc HTML cache local...")

    html_path = Path(HTML_CACHE_PATH)

    if not html_path.exists():
        raise FileNotFoundError(
            f"Không tìm thấy file: {HTML_CACHE_PATH}\n"
            "Hãy mở FBref, Ctrl+S và lưu đúng tên fbref_player_stats.html vào data/raw/"
        )

    html = html_path.read_text(encoding="utf-8", errors="ignore")

    print("Đang parse bảng FBref...")

    table_html = extract_table_html(html, TABLE_ID)

    if not table_html:
        raise Exception(
            "Không tìm thấy bảng stats_standard trong HTML.\n"
            "Có thể bạn lưu nhầm trang Squad Stats thay vì Player Standard Stats."
        )

    df = parse_fbref_table(table_html)

    print("Đang cleaning dữ liệu...")

    df = clean_column_names(df)
    df = remove_repeated_headers(df)
    df = filter_minutes(df, MIN_MINUTES)
    df = clean_nan(df)

    print(f"Số cầu thủ sau khi lọc > {MIN_MINUTES} phút: {len(df)}")

    print("Đang lưu SQLite...")

    save_to_sqlite(df)

    print("DONE")
    print(f"Đã lưu vào database: {DB_PATH}")
    print(f"Tên bảng: {TABLE_NAME}")


if __name__ == "__main__":
    main()