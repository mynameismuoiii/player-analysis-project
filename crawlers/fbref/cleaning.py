import re
import pandas as pd


def normalize_column_name(col: str) -> str:
    col = str(col).strip().lower()
    col = col.replace("%", "pct")
    col = col.replace("+", "_plus_")
    col = col.replace("-", "_")
    col = col.replace("/", "_per_")
    col = re.sub(r"[^\w]+", "_", col)
    col = re.sub(r"_+", "_", col)
    return col.strip("_")


def flatten_soccerdata_df(df: pd.DataFrame, table_name: str) -> pd.DataFrame:
    df = df.reset_index()

    new_cols = []

    for col in df.columns:
        if isinstance(col, tuple):
            parts = [str(c) for c in col if str(c) and "Unnamed" not in str(c)]
            name = "_".join(parts)
        else:
            name = str(col)

        name = normalize_column_name(name)

        if name not in ["player", "team", "league", "season"]:
            name = f"{table_name}_{name}"

        new_cols.append(name)

    df.columns = new_cols
    return df


def clean_df(df: pd.DataFrame, table_name: str) -> pd.DataFrame:
    df = flatten_soccerdata_df(df, table_name)

    # Ép object để thay NaN bằng "N/a" không lỗi Int64
    df = df.astype("object")

    df = df.drop_duplicates()
    df = df.where(pd.notnull(df), "N/a")
    df = df.replace({"": "N/a", "nan": "N/a", "NaN": "N/a"})

    return df


def convert_minutes_to_number(value) -> float:
    value = str(value).replace(",", "").strip()

    try:
        return float(value)
    except Exception:
        return 0


def filter_players_over_90_minutes(df: pd.DataFrame) -> pd.DataFrame:
    min_col = None

    for col in df.columns:
        col_lower = col.lower()

        if (
            col_lower.endswith("_min")
            or col_lower.endswith("_minutes")
            or col_lower == "standard_playing_time_min"
        ):
            min_col = col
            break

    if min_col is None:
        print("Các cột hiện có:")
        print(df.columns.tolist())
        raise ValueError("Không tìm thấy cột số phút thi đấu.")

    df["_minutes_number"] = df[min_col].apply(convert_minutes_to_number)
    df = df[df["_minutes_number"] > 90].copy()
    df = df.drop(columns=["_minutes_number"])

    return df


def make_sqlite_safe(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = [normalize_column_name(c) for c in df.columns]

    seen = {}
    new_cols = []

    for col in df.columns:
        if col not in seen:
            seen[col] = 0
            new_cols.append(col)
        else:
            seen[col] += 1
            new_cols.append(f"{col}_{seen[col]}")

    df.columns = new_cols
    return df