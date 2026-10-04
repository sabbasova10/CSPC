"""
PW2 Lab A -- Motion from tracking data.

Read noisy free-fall position measurements, then:
  - differentiate once  -> velocity
  - differentiate twice -> acceleration (should be ~ constant -g, but noisy!)
  - integrate the acceleration back up -> recover velocity and position

Complete the TODOs. Run:  python analysis.py
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import cumulative_trapezoid

# TODO 1: read freefall.csv into arrays t and y
#         (hint: np.loadtxt with a comma delimiter, skipping the header)

t, y = np.loadtxt("freefall.csv", delimiter=',', skiprows=1, unpack=True)

# TODO 2: compute velocity v = derivative of y w.r.t. t   (np.gradient)
#         and acceleration a = derivative of v w.r.t. t    (np.gradient again)
#         Print the mean acceleration. Is it close to -9.81? Is it noisy?

v = dydt = np.gradient(y, t)
a = dvdt = np.gradient(v, t)
acceleration_mean = np.mean(a)
print(f"Mean acceleration: {acceleration_mean}")
print(f"Standart deviation: {a.std()}")

# TODO 3: integrate a back up to recover velocity and position
#         (hint: cumulative_trapezoid(a, t, initial=0) + v[0], then again)

v_recovered = cumulative_trapezoid(a, t, initial=0) + v[0]
y_recovered = cumulative_trapezoid(v_recovered, t, initial=0) + y[0]
largest_difference = np.max((np.abs(y_recovered-y)))
print(f"Largest difference: {largest_difference}")

# TODO 4: make a figure with 3 stacked panels: position, velocity, acceleration
#         vs time. Mark the true -9.81 line on the acceleration panel.
#         Save it as motion.png


fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(8,6), sharex=True)
a_std = [-9.81]*len(t)

ax1.plot(t, y)
ax1.set_title("Position & time")
ax1.set(xlabel="time (s)", ylabel="position (m)")

ax2.plot(t, v)
ax2.set_title("Velocity & time")
ax2.set(xlabel="time (s)", ylabel="velocity (m)")

ax3.plot(t, a)
ax3.set_title("Acceleration & time")
ax3.plot(t, a_std, linestyle='dashed')
ax3.set(xlabel="time (s)", ylabel="acceleration (m)")

plt.tight_layout()
fig.savefig("motion.png")
