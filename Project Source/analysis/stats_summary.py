import pandas as pd
import sqlite3
from sklearn.preprocessing import StandardScaler

DB_PATH = "data/player_analysis.db"


def load_data():
    conn = sqlite3.connect(DB_PATH)
    stats = pd.read_sql("SELECT * FROM fbref_player_stats", conn)
    values = pd.read_sql("SELECT * FROM player_values", conn)
    conn.close()

    df = stats.merge(values, on=["player", "squad"], how="left")
    return df


def main():
    df = load_data()

    # clean
    df = df.replace("N/a", 0)
    df = df.fillna(0)

    # numeric columns
    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns

    grouped = df.groupby("squad")[numeric_cols]

    mean_df = grouped.mean()
    median_df = grouped.median()
    std_df = grouped.std()

    # save
    mean_df.to_csv("data/processed/mean_stats.csv")
    median_df.to_csv("data/processed/median_stats.csv")
    std_df.to_csv("data/processed/std_stats.csv")

    # find best team
    scaler = StandardScaler()
    scaled = scaler.fit_transform(mean_df)

    mean_df["score"] = scaled.sum(axis=1)
    best_team = mean_df["score"].idxmax()

    print("Best team:", best_team)


if __name__ == "__main__":
    main()