"""
PW2 Lab B Part 5 (bonus) -- find a titration's equivalence point.

titration.csv holds a titration curve: pH versus the volume of base added.
The equivalence point is the volume where the pH changes fastest (the steep
jump). Numerically, that is where the SLOPE of the pH curve is largest.
Run:  python titration.py
"""
import numpy as np
import matplotlib.pyplot as plt

# TODO 1: read titration.csv (columns volume_base, pH) into arrays V, pH.

V, pH = np.loadtxt("titration.csv", delimiter=',', skiprows=1, unpack=True)

# TODO 2: compute the slope of the pH curve with np.gradient(pH, V), and find
#         the volume where that slope is largest (np.argmax). That is the
#         equivalence point. Print it.

dpHdV = np.gradient(pH, V)
eq_point = np.argmax(dpHdV)
V_eq = V[eq_point]
print(f"Equivalence volume: {V_eq}")

# TODO 3: make two plots side by side: (left) pH vs volume with a line at the
#         equivalence point; (right) the slope vs volume, showing it peaks
#         at the equivalence point. Save as titration.png.

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10,4))

ax1.plot(V, pH, label="pH Curve")
ax1.set_xlabel("Volume (ml)")
ax1.set_ylabel("pH")
ax1.axvline(eq_point, linestyle='--', color="red", label="Equvivalence point")
ax1.plot(V_eq, pH[eq_point], 'bo')

ax2.plot(V, dpHdV, label="dpH/dV")
ax2.plot()
ax2.set_xlabel("Volume (ml)")
ax2.set_ylabel("Slope")

ax1.legend()
ax2.legend()

plt.tight_layout()
fig.savefig("titration.png")
plt.show()