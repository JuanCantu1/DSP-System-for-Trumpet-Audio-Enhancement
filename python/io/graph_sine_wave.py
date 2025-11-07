import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

# === Load WAV files ===
sr_flat, flat = wavfile.read(r"C:\Users\johnn\Desktop\DSP Project\New Test\Synthetic\C_flat_253Hz.wav")
sr_ideal, ideal = wavfile.read(r"C:\Users\johnn\Desktop\DSP Project\New Test\Synthetic\C_in-tune_261.63Hz.wav")
sr_mod, mod = wavfile.read(r"C:\Users\johnn\Desktop\DSP Project\New Test\Modified_C_flat_253Hz.wav")

# === Normalize to float for clean comparison ===
flat = flat.astype(np.float32) / 32768
ideal = ideal.astype(np.float32) / 32768
mod = mod.astype(np.float32) / 32768

# === Time axis (zoomed in) ===
zoom_duration = 0.05  # seconds
zoom_samples = int(sr_flat * zoom_duration)
t = np.linspace(0, zoom_duration, zoom_samples, endpoint=False)

# === Plot all three ===
plt.figure(figsize=(14, 6))
plt.plot(t, flat[:zoom_samples], label="Original (Flat)", color='orangered', alpha=0.7)
plt.plot(t, ideal[:zoom_samples], label="Ideal (In-Tune)", color='green', alpha=0.7)
plt.plot(t, mod[:zoom_samples], label="Modified (Autotuned)", color='deepskyblue', linestyle='--', alpha=0.9)

plt.title("Autotune Effect: Flat → Ideal → Modified (Zoomed In)")
plt.xlabel("Time [s]")
plt.ylabel("Amplitude")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
