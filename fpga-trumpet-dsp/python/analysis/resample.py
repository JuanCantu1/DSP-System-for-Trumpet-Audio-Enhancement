import numpy as np
import matplotlib.pyplot as plt
import librosa
import librosa.display
from scipy.io import wavfile
from scipy.signal import resample
import os

# === Load audio ===
orig_path = r"C:\Users\johnn\Desktop\DSP Project\New Test\Inputs\Solo Trumpet Performance by Aiman.wav"
proc_path = r"C:\Users\johnn\Desktop\DSP Project\New Test\Modified_Solo Trumpet Performance by Aiman.wav"

# === Define path for resampled copy ===
resampled_path = r"C:\Users\johnn\Desktop\DSP Project\New Test\Inputs\Solo Trumpet Performance by Aiman_resampled_48kHz.wav"

# === Read WAV files ===
rate_orig, data_orig = wavfile.read(orig_path)
rate_proc, data_proc = wavfile.read(proc_path)

# === Resample if needed ===
target_rate = 48000
if rate_orig != target_rate:
    print("🔁 Resampling original audio to 48kHz...")
    duration = len(data_orig) / rate_orig
    target_len = int(duration * target_rate)
    data_orig_resampled = resample(data_orig, target_len)

    # Save resampled version
    wavfile.write(resampled_path, target_rate, data_orig_resampled.astype(data_orig.dtype))
    print(f"✅ Resampled copy saved to:\n{resampled_path}")
else:
    data_orig_resampled = data_orig

# === Truncate both to same length ===
min_len = min(len(data_orig_resampled), len(data_proc))
data_orig_resampled = data_orig_resampled[:min_len]
data_proc = data_proc[:min_len]

# === Convert to float for librosa ===
orig_float = data_orig_resampled.astype(np.float32)
proc_float = data_proc.astype(np.float32)

# === Compute spectrograms ===
S_orig = librosa.amplitude_to_db(np.abs(librosa.stft(orig_float)), ref=np.max)
S_proc = librosa.amplitude_to_db(np.abs(librosa.stft(proc_float)), ref=np.max)

# === Plot side-by-side ===
plt.figure(figsize=(12, 6))

plt.subplot(2, 1, 1)
librosa.display.specshow(S_orig, sr=target_rate, x_axis='time', y_axis='log')
plt.title("Original (Resampled to 48kHz)")
plt.colorbar(format="%+2.0f dB")

plt.subplot(2, 1, 2)
librosa.display.specshow(S_proc, sr=target_rate, x_axis='time', y_axis='log')
plt.title("Processed Output (48kHz)")
plt.colorbar(format="%+2.0f dB")

plt.tight_layout()
plt.show()
