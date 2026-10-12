import numpy as np
import matplotlib.pyplot as plt


t, x, y = np.loadtxt("trajectory.csv", delimiter=',', skiprows=1, unpack=True)

vx = dxdt = np.gradient(x, t)
vy = dydt = np.gradient(y, t)

ax = dvxdt = np.gradient(vx, t)
ay = dvydt = np.gradient(vy, t)

fig, (ax1, ax2) = plt.subplots(1, 2, sharex=True)

ax1.plot(x, y, label="Trajectory")
ax1.set_title("Path")
ax1.set(xlabel="x (m)", ylabel="y (m)")

speed = np.sqrt(vx**2+vy**2)

ax2.plot(t, speed, label="Speed")
ax2.set_title("Speed & time ")
ax2.set(xlabel="time (s)", ylabel="speed (m/s)")

fig.legend()
fig.savefig("motion_2D.png")
plt.show()