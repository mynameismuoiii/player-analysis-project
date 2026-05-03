import time
import sqlite3
from pathlib import Path
from urllib.parse import quote_plus

import pandas as pd
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

from crawlers.footballtransfers.helpers import (
    normalize_text,
    parse_market_value,
)

from crawlers.footballtransfers.matcher import (
    find_from_top_table,
    find_value_from_page_text,
)


DB_PATH = "data/player_analysis.db"

FBREF_TABLE = "fbref_player_stats"
VALUES_TABLE = "player_values"

CSV_OUTPUT_PATH = "data/processed/player_values.csv"

TOP_VALUES_URL = "https://www.footballtransfers.com/us/values/players/most-valuable-soccer-players"
SEARCH_URL = "https://www.footballtransfers.com/en/search?search_value="


def create_driver():
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options,
    )

    return driver


def read_players_from_db():
    conn = sqlite3.connect(DB_PATH)

    query = f"""
        SELECT DISTINCT player, squad
        FROM {FBREF_TABLE}
        WHERE player IS NOT NULL
          AND player != 'N/a'
          AND player != 'Player'
          AND player != 'Squad Total'
        ORDER BY squad, player
    """

    df = pd.read_sql_query(query, conn)

    conn.close()

    return df


def crawl_top_values_table(driver):
    print("Đang crawl bảng top FootballTransfers...")

    driver.get(TOP_VALUES_URL)

    wait = WebDriverWait(driver, 30)
    wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "table.mvp-table"))
    )

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    table = soup.find("table", class_="mvp-table")

    if table is None:
        print("Không tìm thấy bảng top FootballTransfers.")
        return {}

    top_data = {}

    rows = table.find_all("tr")

    for row in rows:
        cols = row.find_all("td")

        if len(cols) < 3:
            continue

        name_tag = cols[2].find("a")

        if not name_tag:
            continue

        player_name = name_tag.text.strip()
        market_value_text = cols[-1].text.strip()

        if not market_value_text:
            market_value_text = "N/a"

        key = normalize_text(player_name)

        top_data[key] = {
            "matched_name": player_name,
            "market_value_text": market_value_text,
            "market_value_eur": parse_market_value(market_value_text),
            "source_url": TOP_VALUES_URL,
            "status": "TOP_TABLE",
        }

    print(f"Crawl được {len(top_data)} cầu thủ từ bảng top.")

    return top_data


def crawl_one_player_by_search(driver, player_name: str):
    search_url = SEARCH_URL + quote_plus(player_name)

    driver.get(search_url)

    wait = WebDriverWait(driver, 20)
    wait.until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )

    time.sleep(1.5)

    page_text = driver.find_element(By.TAG_NAME, "body").text

    result = find_value_from_page_text(page_text, player_name)

    if not result:
        return {
            "matched_name": "N/a",
            "market_value_text": "N/a",
            "market_value_eur": None,
            "source_url": search_url,
            "status": "NOT_FOUND",
        }

    market_value_text = result["market_value_text"]

    return {
        "matched_name": result["matched_name"],
        "market_value_text": market_value_text,
        "market_value_eur": parse_market_value(market_value_text),
        "source_url": search_url,
        "status": "FOUND_SEARCH",
    }


def crawl_one_player(driver, player_name: str, top_data):
    result = find_from_top_table(player_name, top_data)

    if result is not None:
        return result

    return crawl_one_player_by_search(driver, player_name)


def save_to_sqlite(df):
    conn = sqlite3.connect(DB_PATH)

    df.to_sql(
        VALUES_TABLE,
        conn,
        if_exists="replace",
        index=False,
    )

    conn.close()


def save_to_csv(df):
    Path("data/processed").mkdir(parents=True, exist_ok=True)

    df.to_csv(
        CSV_OUTPUT_PATH,
        index=False,
        encoding="utf-8-sig",
    )


def main():
    print("Đang đọc danh sách cầu thủ từ SQLite...")

    players_df = read_players_from_db()

    if players_df.empty:
        print("Không có dữ liệu cầu thủ.")
        print("Hãy chạy phần I.1 trước.")
        return

    print(f"Số cầu thủ cần crawl giá: {len(players_df)}")

    driver = create_driver()

    results = []

    try:
        top_data = crawl_top_values_table(driver)

        for index, row in players_df.iterrows():
            player = row["player"]
            squad = row["squad"]

            print(f"[{index + 1}/{len(players_df)}] Đang crawl: {player} - {squad}")

            try:
                value_data = crawl_one_player(
                    driver=driver,
                    player_name=player,
                    top_data=top_data,
                )

                results.append({
                    "player": player,
                    "squad": squad,
                    "matched_name": value_data["matched_name"],
                    "market_value_text": value_data["market_value_text"],
                    "market_value_eur": value_data["market_value_eur"],
                    "source_url": value_data["source_url"],
                    "status": value_data["status"],
                })

                print(f"  -> {value_data['status']}: {value_data['market_value_text']}")

            except Exception as e:
                search_url = SEARCH_URL + quote_plus(player)

                results.append({
                    "player": player,
                    "squad": squad,
                    "matched_name": "N/a",
                    "market_value_text": "N/a",
                    "market_value_eur": None,
                    "source_url": search_url,
                    "status": f"ERROR: {str(e)}",
                })

                print(f"  -> ERROR: {e}")

            time.sleep(1)

    finally:
        driver.quit()

    result_df = pd.DataFrame(results)

    print("Đang lưu bảng player_values vào SQLite...")
    save_to_sqlite(result_df)

    print("Đang export CSV...")
    save_to_csv(result_df)

    print("DONE")
    print(f"SQLite table: {VALUES_TABLE}")
    print(f"CSV: {CSV_OUTPUT_PATH}")


if __name__ == "__main__":
    main()