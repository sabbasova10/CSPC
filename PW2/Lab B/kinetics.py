"""
PW2 Lab B Part 3 -- fit a reaction's rate constant to measured data.

A first-order reaction decays as  C(t) = C0 * exp(-k*t).  You have noisy
concentration-vs-time measurements; find the k that best matches them.
Complete the TODOs. Run:  python kinetics.py
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

# TODO 1: read kinetics.csv (columns time, concentration) into arrays t, C.
#         Set C0 = the first concentration.
t, C = np.loadtxt("kinetics.csv", delimiter=",", skiprows=1, unpack=True)
C0 = C[0]

# TODO 2: write total_error(k) = sum of (measured - C0*exp(-k*t))^2.
#         This is the "how bad" number: small when the model matches the data.
def total_error(k):
    return np.sum((C - C0*np.exp(-k*t))**2)

# TODO 3: minimise total_error with scipy.optimize.minimize (method "SLSQP",
#         bounds [(0, 5)], start x0=0.5). Print the fitted k.

result = minimize(total_error, x0=0.5, method="SLSQP", bounds=[(0,5)])
print(f"{result.x[0]:.2f}")
k_fitted = result.x[0]

# TODO 4: plot the measured data (points) and your fitted curve (line) together.
#         Save as kinetics.png.

C_fit = C0 * np.exp(-k_fitted*t)

fig, ax1 = plt.subplots(1,1)
ax1.plot(t, C, color="red", label="Data curve")
ax1.plot(t, C_fit, color="blue", label="Fitted curve")
ax1.set_xlabel="time (s)"
ax1.set_ylabel("concentration")
ax1.set_title("Curve-fitting")

ax1.legend()

fig.savefig("kinetics.png")
plt.show()