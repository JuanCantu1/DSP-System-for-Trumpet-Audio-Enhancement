from scipy.io.wavfile import read
import numpy as np
import os

# === Load the WAV file ===
wav_path = r"C:\Users\johnn\Desktop\DSP Project\New Test\Miniature Etude no 4.wav"
rate, data = read(wav_path)

# === Convert stereo to mono if needed ===
if data.ndim > 1:
    data = data[:, 0]  # Use left channel only

# === Confirm it's 16-bit signed PCM ===
assert data.dtype == np.int16, f"Expected int16 PCM data, got {data.dtype}"

# === Create output .mem file name ===
base_name = os.path.splitext(os.path.basename(wav_path))[0]
mem_filename = f"{base_name}.mem"

# === Write Verilog-compatible .mem file (signed, binary) ===
with open(mem_filename, "w") as f:
    for sample in data:
        f.write(f"{np.uint16(sample):016b}\n")  # Store as 16-bit binary string
