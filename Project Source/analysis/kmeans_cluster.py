import pandas as pd
import sqlite3
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

DB_PATH = "data/player_analysis.db"


def load_data():
    conn = sqlite3.connect(DB_PATH)
    stats = pd.read_sql("SELECT * FROM fbref_player_stats", conn)
    conn.close()
    return stats


def main():
    df = load_data()

    df = df.replace("N/a", 0)
    df = df.fillna(0)

    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns

    X = df[numeric_cols]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    inertia = []
    for k in range(1, 10):
        km = KMeans(n_clusters=k, random_state=42)
        km.fit(X_scaled)
        inertia.append(km.inertia_)

    plt.figure()
    plt.plot(range(1, 10), inertia)
    plt.xlabel("K")
    plt.ylabel("Inertia")
    plt.title("Elbow Method")
    plt.savefig("data/processed/elbow.png")

    kmeans = KMeans(n_clusters=4, random_state=42)
    df["cluster"] = kmeans.fit_predict(X_scaled)

    df.to_csv("data/processed/kmeans_clusters.csv", index=False)

    print("KMeans done")
    print("\nCluster distribution:")
    print(df["cluster"].value_counts())

    print("\nSample data:")
    print(df[["player", "squad", "cluster"]].head(10))


if __name__ == "__main__":
    main()
    