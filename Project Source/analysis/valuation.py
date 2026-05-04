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

    df = df.replace("N/a", 0)
    df = df.fillna(0)

    features = [
        "performance_gls",
        "performance_ast",
        "performance_gplusa",
        "per_90_minutes_gls",
        "per_90_minutes_ast"
    ]

    df[features] = df[features].apply(pd.to_numeric, errors="coerce").fillna(0)

    X = df[features]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    weights = [0.3, 0.2, 0.2, 0.2, 0.1]

    df["estimated_value"] = X_scaled.dot(weights)

    df[["player", "squad", "estimated_value"]].to_csv(
        "data/processed/valuation.csv", index=False
    )

    top_players = df.sort_values("estimated_value", ascending=False).head(10)
    print("\nTop 10 players by estimated value:")
    print(top_players[["player", "squad", "estimated_value"]])


if __name__ == "__main__":
    main()