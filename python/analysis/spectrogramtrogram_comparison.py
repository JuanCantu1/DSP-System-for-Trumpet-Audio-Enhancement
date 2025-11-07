import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import read
from scipy.signal import spectrogram

# === File Paths ===

# original_wav = r"C:\Users\johnn\Desktop\DSP Project\New Test\Inputs\C-Scale.wav"
# processed_wav = r"C:\Users\johnn\Desktop\DSP Project\New Test\Modified_C-Scale.wav"

#original_wav = r"C:\Users\johnn\Desktop\DSP Project\New Test\Solo Trumpet Performance by Aiman_resampled_48kHz.wav"
#processed_wav = r"C:\Users\johnn\Desktop\DSP Project\New Test\Modified_Solo Trumpet Performance by Aiman.wav"

original_wav = r"C:\Users\johnn\Desktop\DSP Project\New Test\Test Complete\Miniature Etude no4\Miniature Etude no 4.wav"
processed_wav = r"C:\Users\johnn\Desktop\DSP Project\New Test\Test Complete\Miniature Etude no4\processed_output.wav"

# === Load WAV Files ===
def load_wav(path):
    rate, data = read(path)
    if data.ndim > 1:
        data = data[:, 0]  # mono
    return rate, data

rate_orig, orig = load_wav(original_wav)
rate_proc, proc = load_wav(processed_wav)

# === Sanity Check ===
assert rate_orig == rate_proc, "Sample rates do not match!"

# === Spectrogram Settings ===
nperseg = 8192
noverlap = 6144

# === Compute Spectrograms ===
f1, t1, Sxx1 = spectrogram(orig, fs=rate_orig, nperseg=nperseg, noverlap=noverlap)
f2, t2, Sxx2 = spectrogram(proc, fs=rate_proc, nperseg=nperseg, noverlap=noverlap)

# === Plot ===
plt.figure(figsize=(16, 6))

# --- Original ---
plt.subplot(1, 2, 1)
plt.pcolormesh(t1, f1, 10 * np.log10(Sxx1 + 1e-10), shading='gouraud')
plt.title("Original Audio Spectrogram")
plt.xlabel("Time [s]")
plt.ylabel("Frequency [Hz]")
plt.ylim(0, 4000)  # Limit to musical range
plt.colorbar(label="Power (dB)")

# --- Processed ---
plt.subplot(1, 2, 2)
plt.pcolormesh(t2, f2, 10 * np.log10(Sxx2 + 1e-10), shading='gouraud')
plt.title("Processed Audio Spectrogram")
plt.xlabel("Time [s]")
plt.ylabel("Frequency [Hz]")
plt.ylim(0, 4000)
plt.colorbar(label="Power (dB)")

plt.tight_layout()
plt.show()
