import pandas as pd


def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    new_columns = []

    for col in df.columns:
        col = str(col).strip()

        col = col.replace(" ", "_")
        col = col.replace("/", "_")
        col = col.replace("-", "_")
        col = col.replace("%", "percent")
        col = col.replace("+", "plus")
        col = col.replace("#", "no")
        col = col.replace(".", "")
        col = col.lower()

        new_columns.append(col)

    df.columns = new_columns

    return df


def remove_repeated_headers(df: pd.DataFrame) -> pd.DataFrame:
    if "player" in df.columns:
        df = df[df["player"] != "Player"]

    return df


def filter_minutes(df: pd.DataFrame, min_minutes: int = 90) -> pd.DataFrame:
    minute_col = None

    for col in df.columns:
        if col == "playing_time_min" or col.endswith("_min") or col == "min":
            minute_col = col
            break

    if minute_col is None:
        print("Không tìm thấy cột phút thi đấu, bỏ qua bước lọc.")
        return df

    df[minute_col] = (
        df[minute_col]
        .astype(str)
        .str.replace(",", "", regex=False)
    )

    df[minute_col] = pd.to_numeric(df[minute_col], errors="coerce")

    df = df[df[minute_col] > min_minutes]

    return df


def clean_nan(df: pd.DataFrame) -> pd.DataFrame:
    return df.fillna("N/a")