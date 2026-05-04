import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

DATA_PATH = "data/processed/kmeans_clusters.csv"


def main():
    df = pd.read_csv(DATA_PATH)

    df = df.replace("N/a", 0)
    df = df.fillna(0)

    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns
    numeric_cols = [col for col in numeric_cols if col != "cluster"]

    X = df[numeric_cols]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    pca_2d = PCA(n_components=2)
    X_pca_2d = pca_2d.fit_transform(X_scaled)

    plt.figure()
    scatter = plt.scatter(
        X_pca_2d[:, 0],
        X_pca_2d[:, 1],
        c=df["cluster"]
    )
    plt.title("PCA 2D (colored by cluster)")
    plt.xlabel("PC1")
    plt.ylabel("PC2")
    plt.colorbar(scatter)

    plt.savefig("data/processed/pca_2d.png")
    plt.close()

    pca_3d = PCA(n_components=3)
    X_pca_3d = pca_3d.fit_transform(X_scaled)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")

    scatter = ax.scatter(
        X_pca_3d[:, 0],
        X_pca_3d[:, 1],
        X_pca_3d[:, 2],
        c=df["cluster"]
    )

    ax.set_title("PCA 3D (colored by cluster)")
    ax.set_xlabel("PC1")
    ax.set_ylabel("PC2")
    ax.set_zlabel("PC3")

    fig.colorbar(scatter)

    plt.savefig("data/processed/pca_3d.png")
    plt.close()

    print("PCA done")

    print("\nExplained variance ratio (2D):")
    print(pca_2d.explained_variance_ratio_)

    print("\nSample PCA data:")
    sample_df = pd.DataFrame({
        "player": df["player"].head(10),
        "cluster": df["cluster"].head(10),
        "PC1": X_pca_2d[:10, 0],
        "PC2": X_pca_2d[:10, 1],
    })
    print(sample_df)


if __name__ == "__main__":
    main()