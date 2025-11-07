import numpy as np
from scipy.io.wavfile import write
import os

# === Settings ===
duration = 10.0        # seconds
sample_rate = 48000    # Hz
amplitude = 0.8        # Signal amplitude

# === Frequencies ===
flat_freq = 253.0      # Slightly flat
sharp_freq = 270.0     # Slightly sharp

# === Time array ===
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

# === Generate sine wave function ===
def generate_sine(freq, label):
    sine_wave = (amplitude * np.sin(2 * np.pi * freq * t)).astype(np.float32)
    sine_int16 = (sine_wave * 32767).astype(np.int16)
    filename = f"{label}_note.wav"
    filepath = os.path.join(r"C:\Users\johnn\Desktop\DSP Project\New Test", filename)
    write(filepath, sample_rate, sine_int16)
    print(f"✅ {label.capitalize()} tone saved: {filepath}")

# === Generate both versions ===
generate_sine(flat_freq, "flat_C")
generate_sine(sharp_freq, "sharp_C")
