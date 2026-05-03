from io import StringIO

import pandas as pd
from bs4 import BeautifulSoup, Comment


def extract_table_html(page_source: str, table_id: str = "stats_standard"):
    soup = BeautifulSoup(page_source, "html.parser")

    # 1. Tìm đúng id trước
    table = soup.find("table", id=table_id)
    if table:
        return str(table)

    # 2. FBref đôi khi giấu table trong comment
    comments = soup.find_all(string=lambda text: isinstance(text, Comment))

    for comment in comments:
        comment_soup = BeautifulSoup(comment, "html.parser")
        table = comment_soup.find("table", id=table_id)
        if table:
            return str(table)

    # 3. Fallback: tìm bảng nào có cột Player, Squad, Min
    all_tables = soup.find_all("table")

    for table in all_tables:
        text = table.get_text(" ", strip=True)
        if "Player" in text and "Squad" in text and "Min" in text:
            return str(table)

    for comment in comments:
        comment_soup = BeautifulSoup(comment, "html.parser")
        all_tables = comment_soup.find_all("table")

        for table in all_tables:
            text = table.get_text(" ", strip=True)
            if "Player" in text and "Squad" in text and "Min" in text:
                return str(table)

    return None


def parse_fbref_table(table_html: str) -> pd.DataFrame:
    tables = pd.read_html(StringIO(table_html))

    if not tables:
        raise Exception("Không parse được bảng FBref")

    df = tables[0]

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [
            "_".join([str(x) for x in col if "Unnamed" not in str(x)]).strip()
            for col in df.columns
        ]

    return df