import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats


df = pd.read_csv("heart.csv")
print(f"Rows & Columns: {df.shape}")
df.head()

# print(df.iloc[:,:4])

age = df["age"]
chol = df["chol"]
trestbps = df["trestbps"]
thalach = df["thalach"]
target = df["target"]

columns = ["age", "chol", "trestbps", "thalach"]

print(df[columns].describe())

fig, ax = plt.subplots(2, 4, figsize=(10,10))

for i, column in enumerate(columns):
    ax[0,i].hist(df[column], color="black", edgecolor="white")
    ax[0,i].set_title(f"Histogram: {column}")
   
    stats.probplot(df[column], dist="norm", plot=ax[1,i])
    ax[1, i].set_title(column)

plt.tight_layout()
fig.savefig("distribution.png")

for column in columns:
    W, p = stats.shapiro(df[column])
    if p < 0.05:
        print(f"{column} - not normal")
        print(f"W = {W:.2f}; p = {p:.2e}\n")
    else:
        print(f"{column} - normal")