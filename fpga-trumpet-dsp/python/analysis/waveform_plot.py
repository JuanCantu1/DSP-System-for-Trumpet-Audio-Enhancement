import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import read

# === Load WAV file ===
rate, data = read(r"C:\Users\johnn\Desktop\DSP Project\New Test\C_note_sine_10s.wav")

# === Normalize to [-1, 1] for plotting if needed ===
signal = data / 32768.0  # since it’s int16

# === Time vector for plotting ===
t = np.linspace(0, len(signal) / rate, num=len(signal), endpoint=False)

# === Plotting (Zoomed-In) ===
zoom_samples = 1000  # Show a few cycles
plt.figure(figsize=(10, 4))
plt.plot(t[:zoom_samples], signal[:zoom_samples], label="Sine Wave", color='lime')
plt.title("261.63 Hz Sine Wave")
plt.xlabel("Time [s]")
plt.ylabel("Amplitude")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
