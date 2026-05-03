from io import StringIO

import pandas as pd
from bs4 import BeautifulSoup, Comment


def extract_tables_from_html(html: str) -> list[pd.DataFrame]:
    soup = BeautifulSoup(html, "html.parser")
    tables: list[pd.DataFrame] = []

    # Bảng HTML bình thường
    for table in soup.find_all("table"):
        try:
            tables.extend(pd.read_html(StringIO(str(table))))
        except ValueError:
            pass

    # Bảng bị FBref giấu trong comment <!-- table -->
    comments = soup.find_all(string=lambda text: isinstance(text, Comment))

    for comment in comments:
        if "<table" not in comment:
            continue

        comment_soup = BeautifulSoup(comment, "html.parser")

        for table in comment_soup.find_all("table"):
            try:
                tables.extend(pd.read_html(StringIO(str(table))))
            except ValueError:
                pass

    return tables


def get_player_table(html: str) -> pd.DataFrame:
    tables = extract_tables_from_html(html)

    for df in tables:
        if isinstance(df.columns, pd.MultiIndex):
            cols = [col[-1] for col in df.columns]
        else:
            cols = list(df.columns)

        if "Player" in cols and "Squad" in cols:
            return df

    raise Exception("Không tìm thấy bảng cầu thủ có cột Player và Squad")