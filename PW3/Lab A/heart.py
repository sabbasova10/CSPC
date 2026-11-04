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
        
desease = thalach[target==1]
healthy = thalach[target==0]

u_stat, p = stats.mannwhitneyu(desease, healthy)
print(f"\nU={u_stat:.2f}; p={p:.2e}")
if p < 0.05:
    print(f"thalach groups differ significantly")
else:
    print(f"thalach do not differ")

d_mean = desease.mean()
d_se = desease.std(ddof=1)/np.sqrt(len(desease))
d_low, d_high = d_mean - 2*d_se, d_mean + 2*d_se

print(f"Desease: mean={d_mean:.2f}; SE={d_se:.2f}; CI=[{d_low:.2f},{d_high:.2f}]")

h_mean = healthy.mean()
h_se = healthy.std(ddof=1)/np.sqrt(len(healthy))
h_low, h_high = h_mean - 2*h_se, h_mean + 2*h_se

print(f"Healthy: mean={h_mean:.2f}; SE={h_se:.2f}; CI=[{h_low:.2f},{h_high:.2f}]")

fig, ax = plt.subplots(1, 1, figsize=(10,8))
ax.bar(["Healthy (0)", "Disease (1)"], [h_mean, d_mean],
yerr=[2 * h_se, 2 * d_se], capsize=5,
color=["green", "red"], edgecolor="black", alpha=0.8)
fig.savefig("barchart.png")
plt.show()

r, p = stats.pearsonr(age, thalach)
print(f"r={r:.4f}, p={p:.2e}"))

fig, ax = plt.subplots(1,1, figsize=(8,8))
ax.scatter(age, thalach, alpha=0.5, label="Corilation of age and max heart beat")
ax.legend()
fig.savefig("corilation.png")
plt.show()


p_target = df["target"].value_counts(normalize=True)
p_sex = df["sex"].value_counts(normalize=True)

print(p_target)
print(p_sex)

target_entropy = -np.sum(p_target*np.log2(p_target))
print(f"Target Entropy: {target_entropy:.2f}")