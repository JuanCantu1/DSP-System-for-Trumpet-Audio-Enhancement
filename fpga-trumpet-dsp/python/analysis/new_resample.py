import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import read, write
from scipy.signal import spectrogram, resample_poly
from math import gcd

# === File Paths ===
original_wav  = r"C:\Users\johnn\Desktop\DSP Project\New Test\Test Complete\Miniature Etude no4\Miniature Etude no 4.wav"
processed_wav = r"C:\Users\johnn\Desktop\DSP Project\New Test\processed_output.wav"

# === Load as mono, pick the non-silent channel ===
def load_mono(path):
    rate, data = read(path)
    print(f"\nLoading '{path}' → rate={rate}, shape={data.shape}, dtype={data.dtype}")
    if data.ndim > 1:
        ptp = np.ptp(data, axis=0)
        chan = np.argmax(ptp)
        data = data[:, chan]
        print(f"  → Using channel #{chan} (peak-to-peak = {ptp[chan]})")
    return rate, data.astype(np.float64)

rate_o, orig = load_mono(original_wav)
rate_p, proc = load_mono(processed_wav)

# === Raw stats before resample ===
print("\nRAW STATS:")
print(" Original: min/max/mean =", orig.min(), orig.max(), orig.mean())
print(" Processed:",             proc.min(), proc.max(), proc.mean())

# === Resample processed → original rate using GCD‐reduced factors ===
if rate_p != rate_o:
    print(f"\nResampling from {rate_p} → {rate_o} Hz …")
    g    = gcd(rate_o, rate_p)
    up   = rate_o // g
    down = rate_p // g
    print(f"  • up={up}, down={down}")
    proc = resample_poly(proc, up, down)
    rate_p = rate_o

# === Stats after resample ===
print("\nPOST-RESAMPLE STATS:")
print(" Processed: min/max/mean =", proc.min(), proc.max(), proc.mean())
print(f" Duration: original = {len(orig)/rate_o:.2f}s, processed = {len(proc)/rate_p:.2f}s")

# === Zero-center & normalize processed to original’s peak ===
orig -= np.mean(orig)
proc -= np.mean(proc)
peak_o = np.max(np.abs(orig))
peak_p = np.max(np.abs(proc))
if peak_p > 0:
    proc *= (peak_o/peak_p)
print("\nAFTER NORMALIZATION:")
print(" Processed peak now matches original:", np.max(np.abs(proc)))

# === Spectrogram parameters ===
nperseg, noverlap = 8192, 6144

# Compute spectrograms
f1, t1, S1 = spectrogram(orig, fs=rate_o,    nperseg=nperseg, noverlap=noverlap)
f2, t2, S2 = spectrogram(proc, fs=rate_p,    nperseg=nperseg, noverlap=noverlap)

# === Plot full-length spectrograms ===
plt.figure(figsize=(16,6))

# Original
plt.subplot(1,2,1)
plt.pcolormesh(t1, f1, 10*np.log10(S1 + 1e-10), shading='gouraud',
               vmin=-80, vmax=50)
plt.title("Original Audio Spectrogram")
plt.xlabel("Time [s]")
plt.ylabel("Frequency [Hz]")
plt.ylim(0,4000)
plt.colorbar(label="Power (dB)")

# Processed
plt.subplot(1,2,2)
plt.pcolormesh(t2, f2, 10*np.log10(S2 + 1e-10), shading='gouraud',
               vmin=-80, vmax=50)
plt.title("Processed Audio Spectrogram")
plt.xlabel("Time [s]")
plt.ylabel("Frequency [Hz]")
plt.ylim(0,4000)
plt.colorbar(label="Power (dB)")

plt.tight_layout()
plt.show()

# === Optional: write out the debug resampled/normalized copy ===
debug_out = processed_wav.replace(".wav", "_debug_resampled.wav")
write(debug_out, rate_p, proc.astype(np.int16))
print(f"\nWrote debug copy to: {debug_out}")
