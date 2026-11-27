import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import filtfilt, butter, find_peaks, spectrogram
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

# 1
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

# 2
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

# 3

a = 0.5
b = 10

Z_clean = bandpass(Z, fs, a, b)
N_clean = bandpass(N, fs, a, b)
E_clean = bandpass(E, fs, a, b)

print(np.allclose(np.fft.ifft(np.fft.fft(Z)).real, Z))

fig, ax1 = plt.subplots(1, 1, figsize=(10, 4))
ax1.plot(t, (Z - Z_clean) * 1000, color="blue", linewidth=0.7)
ax1.set_title("Removed Component (Z - Z_clean): Outside 0.5–10 Hz")
ax1.set_xlabel("Time (s)")
ax1.set_ylabel("Velocity (mm/s)")
ax1.grid(True, linestyle="--", alpha=0.5)
plt.tight_layout()
fig.savefig("results/removed_Z.png")
plt.show()

# 4

H_clean = np.sqrt(N_clean**2 + E_clean**2)
w_05 = int(0.5 * fs)
env_Z = np.convolve(np.abs(Z_clean), np.ones(w_05) / w_05, mode="same")
env_H = np.convolve(H_clean, np.ones(w_05) / w_05, mode="same")

windows = [
    (0.05, "0.05 s (too short)"),
    (0.5,  "0.5 s (just right)"),
    (5.0,  "5.0 s (too long)"),
]

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(t, np.abs(Z_clean) * 1000, color="black", linewidth=0.5, label="|Z_clean|")

for sec, label in windows:
    w = int(sec * fs)
    env = np.convolve(np.abs(Z_clean), np.ones(w) / w, mode="same")
    ax.plot(t, env * 1000, linewidth=1.2, label=label)

ax.set_xlabel("Time (s)")
ax.set_ylabel("Amplitude (mm/s)")
ax.set_title("Effect of Smoothing Window Length on Z Envelope")
ax.legend()
ax.grid(True, linestyle="--", alpha=0.5)

plt.tight_layout()
fig.savefig("results/envelopes.png", dpi=150)
plt.show()

# 5
tp = t[np.argmax(env_Z > 0.05 * np.max(env_Z))]

mask_s = t >= tp + 2
ts = t[mask_s][np.argmax(env_H[mask_s] > 0.1 * np.max(env_H))]
print(tp, ts)

channels = [Z_clean, N_clean, E_clean]
names = ["Z", "N", "E"]

fig, axes = plt.subplots(3, 1, figsize=(10, 8), sharex=True)
for i, channel in enumerate(channels):
    axes[i].plot(t, channel * 1000, label=names[i])
    axes[i].axvline(tp, color="blue", linestyle="--", label="tp")
    axes[i].axvline(ts, color="red", linestyle="--", label="ts")
    axes[i].legend(loc="upper right")

plt.tight_layout()
fig.savefig("results/arrivals.png")
plt.show()

peaks, _ = find_peaks(env_H, prominence=0.2 * np.max(env_H), distance=int(2 * fs))
ts_max = t[peaks[np.argmax(env_H[peaks])]]
print(ts_max)

# 6
R = (ts - tp) / ((1 / vs) - (1 / vp))
dR = 1.0 / ((1 / vs) - (1 / vp))
t_origin = tp - R / vp
print(f"R = {R:.2f} ± {dR:.2f} km\nt origin: {t_origin}")

# 7
f, tt, S = spectrogram(Z, fs, nperseg=256)
mask_f = f <= 10

fig, ax = plt.subplots(figsize=(10, 5))
pcm = ax.pcolormesh(tt, f[mask_f], 10 * np.log10(S[mask_f, :]), shading="auto")
ax.set_xlabel("Time (s)")
ax.set_ylabel("Frequency (Hz)")
ax.set_title("Spectrogram of Raw Z Channel (0–10 Hz)")
fig.colorbar(pcm, ax=ax, label="Power (dB)")
# plt.ylim(0, 10)
plt.tight_layout()
fig.savefig("results/spectrogram.png", dpi=150)
plt.show()