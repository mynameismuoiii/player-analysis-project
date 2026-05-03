import pandas as pd


ID_COLUMNS = {
    "Rk",
    "Player",
    "Nation",
    "Pos",
    "Squad",
    "Age",
    "Born",
    "Comp",
}


def flatten_columns(df: pd.DataFrame, prefix: str) -> pd.DataFrame:
    if not isinstance(df.columns, pd.MultiIndex):
        return df

    new_columns = []

    for col in df.columns:
        col_name = col[-1]

        if col_name in ID_COLUMNS:
            new_columns.append(col_name)
        else:
            new_columns.append(f"{prefix}_{col_name}")

    df.columns = new_columns

    return df


def remove_repeated_header_rows(df: pd.DataFrame) -> pd.DataFrame:
    if "Rk" in df.columns:
        df = df[df["Rk"].astype(str) != "Rk"]

    if "Player" in df.columns:
        df = df[df["Player"].astype(str) != "Player"]

    return df


def clean_table(df: pd.DataFrame, prefix: str) -> pd.DataFrame:
    df = flatten_columns(df, prefix)
    df = remove_repeated_header_rows(df)

    df = df.drop(columns=["Rk"], errors="ignore")
    df = df.loc[:, ~df.columns.duplicated()]

    df = df.fillna("N/a")

    return df


def filter_minutes_over_90(df: pd.DataFrame) -> pd.DataFrame:
    if "Min" not in df.columns:
        raise Exception("Không tìm thấy cột Min trong bảng standard")

    df = df.copy()

    df["Min"] = (
        df["Min"]
        .astype(str)
        .str.replace(",", "", regex=False)
    )

    df["Min"] = pd.to_numeric(df["Min"], errors="coerce")

    df = df[df["Min"] > 90]

    return df


def final_clean(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df = df.fillna("N/a")
    df = df.replace(["", "nan", "NaN", "None", None], "N/a")

    return df