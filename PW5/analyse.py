import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import filtfilt, butter
import os

def bandpass(x, fs, a, b):
    N_samples = len(x)
    X = np.fft.fft(x)
    f = np.fft.fftfreq(N_samples, d=1/fs)
    X[(np.abs(f) < a) | (np.abs(f) > b)] = 0  # delete everything outside a..b Hz
    return np.fft.ifft(X).real
    #
    # b, a = butter(4, [a,b], btype="band", fs=fs)
    # X[(np.abs(f) < a) | (np.abs(f) > b)] = 0 
    
    

os.makedirs("results", exist_ok=True)

d = pd.read_csv("data/seismogram_A.csv")
t = d["time_s"].to_numpy()
Z = d["Z"].to_numpy()
N = d["N"].to_numpy()
E = d["E"].to_numpy()

fs = 1/(t[1]-t[0])

fig, (ax1, ax2, ax3) = plt.subplots(1, 3, sharex=True, figsize=(8,10))

ax1.plot(t, Z, label="Vertical & time")
ax2.plot(t, N, label="North-south & time")
ax3.plot(t, E, label="East-west & time")

fig.legend()
plt.tight_layout()
fig.savefig("results/channels_on_time.png")
plt.show()

fs = 1/(t[1]-t[0])

vp=6.2
vs=3.6

mask_60 = t <= 60

fig, axes = plt.subplots(3,1, sharex=True)
axes[0].plot(t[mask_60], Z[mask_60]*1000 , label="Vertical channel")
axes[1].plot(t[mask_60], N[mask_60]*1000, label="North-South channel")
axes[2].plot(t[mask_60], E[mask_60]*1000, label="East-West channel")

plt.tight_layout()
fig.savefig("results/time_dependencies.png")
plt.show()

X = np.fft.fft(Z)
f = np.fft.fftfreq(len(Z), d=1/fs)
amp = np.abs(X)/len(Z)*2

indexes = np.arange(0,len(Z))

fig, axes = plt.subplots(1, 2)
axes[0].plot(indexes, amp)
axes[1].plot(f, amp)
plt.show()

Z_quiet = Z[mask_60]
N_quiet = len(Z_quiet)
X_quiet = np.fft.fft(Z_quiet)
f_quiet = np.fft.fftfreq(N_quiet, d=1/fs)
amp_quiet = np.abs(X_quiet) / N_quiet * 2

pos_quiet = f_quiet > 0
pos_full = f > 0

fig, ax1 = plt.subplots(1, 1, figsize=(9, 5))

ax1.loglog(f[pos_full], amp[pos_full], label="Whole spectrum", alpha=0.85, linewidth=0.8)
ax1.loglog(f_quiet[pos_quiet], amp_quiet[pos_quiet], label="Quiet Part", alpha=0.85, linewidth=0.8)

ax1.set_xlabel("Frequency (Hz)")
ax1.set_ylabel("Amplitude (m/s)")
ax1.set_title("Z spectrum")
ax1.legend()
ax1.grid(True, which="both", linestyle="--", alpha=0.4)

plt.tight_layout()
fig.savefig("results/loglog_spectrum.png", dpi=150)
plt.show()