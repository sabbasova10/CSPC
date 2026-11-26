from sklearn.datasets import load_wine
from sklearn.decomposition import PCA
import pandas as pd
import os

import numpy as np

from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.pipeline import make_pipeline
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

os.makedirs("results", exist_ok=True)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 1000)

wine = load_wine(as_frame=True)
X = wine.data # DataFrame, 178 rows x 13 measurements
cultivar = wine.target # Series of 0/1/2 -- set aside until B6

# B1
print(wine.DESCR)
stats = X.describe().T[["min", "max", "mean", "std"]]
stats["range"] = stats["max"] - stats["min"]
print(stats.sort_values("std", ascending=False))
# largest: propoline, magnesium
# smallest:  Nonflavanoid Phenols, Hue

# B2
pca_raw = PCA()
pca_raw.fit(X)

for i, ratio in enumerate(pca_raw.explained_variance_ratio_, start=1):
    print(f"PC{i}: {ratio:.4f}")

pc1_loadings = pd.Series(pca_raw.components_[0], index=X.columns).sort_values(ascending=False)
print("\nPC1 Loadings (sorted)")
print(pc1_loadings)

# B3
scaler = StandardScaler(with_mean=True, with_std=True)
Z = scaler.fit_transform(X) 

print("B3) Scaling Check")
print("Column means (max abs):", np.max(np.abs(Z.mean(axis=0))))
print("Column stds  (min, max):", Z.std(axis=0).min(), Z.std(axis=0).max())

pca = PCA()
scores = pca.fit_transform(Z)

exp_var = pca.explained_variance_ratio_
cum_var = np.cumsum(exp_var)

variance_df = pd.DataFrame({
    "PC": [f"PC{i}" for i in range(1, len(exp_var) + 1)],
    "explained_variance_ratio": np.round(exp_var, 4),
    "cumulative_variance": np.round(cum_var, 4),
})

print("\nB3) Explained Variance & Cumulative Sums")
print(variance_df.to_string(index=False))

n_90 = int(np.argmax(cum_var >= 0.90)) + 1
print(f"\nComponents needed to keep >= 90% variance: {n_90} ({cum_var[n_90 - 1]:.4f})")
print(f"Variance kept by PC1–PC2 plane: {cum_var[1]:.4f})")

loadings_df = pd.DataFrame({
    "PC1_loading": np.round(pca.components_[0], 4),
    "PC2_loading": np.round(pca.components_[1], 4),
}, index=X.columns)

print("\nB3) PC1 & PC2 Loadings (sorted by PC1)")
print(loadings_df.sort_values("PC1_loading", ascending=False))

print("\nB3) PC1 & PC2 Loadings (sorted by PC2)")
print(loadings_df.sort_values("PC2_loading", ascending=False))

pcs = np.arange(1, len(exp_var) + 1)

fig, ax = plt.subplots(figsize=(8, 5))
ax.bar(pcs, exp_var, alpha=0.7, label="Individual explained variance")
ax.plot(pcs, cum_var, marker="o", color="red", label="Cumulative explained variance")
ax.axhline(0.9, color="green", linestyle="--", label="90% threshold")
ax.set_xticks(pcs)
ax.set_title("PCA Scree Plot")
ax.set_ylabel("Explained Variance Ratio")
ax.set_xlabel("Principal Components")
ax.grid(True, linestyle="--", alpha=0.5)
ax.legend()
plt.tight_layout()
fig.savefig("results/scree.png", dpi=150)
plt.show()

fig, ax = plt.subplots(1, 1, figsize=(7, 5))
ax.scatter(scores[:, 0], scores[:, 1], color="steelblue", alpha=0.8, edgecolors="k")
ax.set_xlabel(f"PC1 ({exp_var[0]*100:.1f}% variance)")
ax.set_ylabel(f"PC2 ({exp_var[1]*100:.1f}% variance)")
ax.set_title("Wines in the PC1–PC2 Plane (Unlabelled)")
ax.grid(True, linestyle="--", alpha=0.5)
plt.tight_layout()
fig.savefig("results/pc1_pc2.png", dpi=150)
plt.show()