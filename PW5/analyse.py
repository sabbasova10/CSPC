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


def analyse(csv_file):
    
    d = pd.read_csv(csv_file)
    t = d["time_s"].to_numpy()
    Z = d["Z"].to_numpy()
    N = d["N"].to_numpy()
    E = d["E"].to_numpy()

    fs = 1/(t[1]-t[0])
    
    # 3
    
    vp=6.2
    vs=3.6
    a = 0.5
    b = 10

    Z_clean = bandpass(Z, fs, a, b)
    N_clean = bandpass(N, fs, a, b)
    E_clean = bandpass(E, fs, a, b)

    # 4

    H_clean = np.sqrt(N_clean**2 + E_clean**2)
    w_05 = int(0.5 * fs)
    env_Z = np.convolve(np.abs(Z_clean), np.ones(w_05) / w_05, mode="same")
    env_H = np.convolve(H_clean, np.ones(w_05) / w_05, mode="same")

    # 5
    tp = t[np.argmax(env_Z > 0.05 * np.max(env_Z))]

    mask_s = t >= tp + 2
    ts = t[mask_s][np.argmax(env_H[mask_s] > 0.1 * np.max(env_H))]
    print(tp, ts)

    peaks, _ = find_peaks(env_H, prominence=0.2 * np.max(env_H), distance=int(2 * fs))
    ts_max = t[peaks[np.argmax(env_H[peaks])]]
    print(ts_max)

    # 6
    R = (ts - tp) / ((1 / vs) - (1 / vp))
    dR = 1.0 / ((1 / vs) - (1 / vp))
    t_origin = tp - R / vp
    print(f"R = {R:.2f} ± {dR:.2f} km\nt origin: {t_origin}")

    # 8
    H_raw = np.sqrt(N**2 + E**2)
    PGV = np.max(H_raw) * 100
    M = (np.log10(PGV) + np.log10(R) + 1.0)/0.55
    print(f"PGV = {PGV:.4f} cm/s, M = {M:.2f}")
    
    return {"Record": csv_file, "tp":tp, "ts": ts, "Distance": R, "Peak Ground Velocity": PGV, "Magnitude": M}


if __name__ == "__main__":
    row1 = analyse("data/seismogram_A.csv")
    row2 = analyse("data/seismogram_B.csv")

    df = pd.DataFrame([row1,row2])

    df.to_csv("results/events.csv", index=False)