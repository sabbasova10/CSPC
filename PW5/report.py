import pandas as pd
import os

os.makedirs("results", exist_ok=True)

df = pd.read_csv("results/events.csv")

lines = [f"**SEISMOGRAM ANALYSIS REPORT**  "]

for _, row in df.iterrows():
    lines.append(f"Record: **{row['Record']}**  ")
    lines.append(f"P-wave arrival (t_P): {row['tp']:.2f} s  ")
    lines.append(f"S-wave arrival (t_S): {row['ts']:.2f} s  ")
    lines.append(f"Distance (R): {row['Distance']:.2f} km  ")
    lines.append(f"Peak Ground Velocity: {row['Peak Ground Velocity']:.4f} cm/s  ")
    lines.append(f"Magnitude (M): {row['Magnitude']:.2f}  ")
    lines.append("")

closest = df.loc[df["Distance"].idxmin()]
strongest = df.loc[df["Magnitude"].idxmax()]

lines.append(f"**SUMMARY**  ")
lines.append(f"Closest event: **{closest['Record']}** ({closest['Distance']:.2f} km)  ")
lines.append(f"Strongest event: **{strongest['Record']}** (M {strongest['Magnitude']:.2f})  ")

with open("results/report.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")