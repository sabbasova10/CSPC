import pandas as pd
from scipy import stats


df = pd.read_csv("chemicals_cancer.csv")

benzene = df["benzene"]
cadmium = df["cadmium"]
malignancy = df["malignancy"]

r_b, p_b = stats.pearsonr(benzene, malignancy)
r_c, p_c = stats.pearsonr(cadmium, malignancy)

print(f"Benzen: r={r_b:.4f}, p={p_b:.2e}")
print(f"Cadmium: r={r_c:.4f}, p={p_c:.2e}\n")

age = df["age"]
pollution_index =  df["pollution_index"]

r_age, p_age = stats.pearsonr(age, malignancy)
r_pol, p_pol = stats.pearsonr(pollution_index, malignancy)

print(f"Age: r={r_age:.4f}, p={p_age:.2e}")
print(f"Pollution: r={r_pol:.4f}, p={p_pol:.2e}\n")

standart_restriction_df = df[(pollution_index >= 40) & (pollution_index <= 60)]
narrow_restriction_df = df[(pollution_index >= 45) & (pollution_index <= 55)]

r_b, p_b = stats.pearsonr(standart_restriction_df["benzene"], standart_restriction_df["malignancy"])
r_c, p_c = stats.pearsonr(standart_restriction_df["cadmium"], standart_restriction_df["malignancy"])

print("Standart restrictions")
print(f"Benzen: r={r_b:.4f}, p={p_b:.2e}")
print(f"Cadmium: r={r_c:.4f}, p={p_c:.2e}\n")

r_b, p_b = stats.pearsonr(narrow_restriction_df["benzene"], narrow_restriction_df["malignancy"])
r_c, p_c = stats.pearsonr(narrow_restriction_df["cadmium"], narrow_restriction_df["malignancy"])

print("Narrow restrictions")
print(f"Benzen: r={r_b:.4f}, p={p_b:.2e}")
print(f"Cadmium: r={r_c:.4f}, p={p_c:.2e}\n")