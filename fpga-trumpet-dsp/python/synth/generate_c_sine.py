import numpy as np
from scipy.io.wavfile import write

# === Parameters ===
duration = 10  # seconds
sample_rate = 48000  # Hz
frequency = 261.63  # C4 in Hz

# === Time and Signal ===
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
signal = 0.9 * np.sin(2 * np.pi * frequency * t)  # 90% of max amplitude

# === Convert to 16-bit PCM and Save ===
pcm = np.int16(signal * 32767)
write("C_note_sine_10s.wav", sample_rate, pcm)
print("✅ Saved: C_note_sine_10s.wav")
