import numpy as np
import matplotlib.pyplot as plt
import os

# === Paths ===

# original_path = r"C:\Users\johnn\Desktop\DSP Project\New Test\C-Scale.mem"
# processed_path = r"C:\Users\johnn\Desktop\DSP Project\New Test\Modified_C-Scale.mem"

#original_path = r"C:\Users\johnn\Desktop\DSP Project\New Test\Solo Trumpet Performance by Aiman.mem"
#processed_path = r"C:\Users\johnn\Desktop\DSP Project\New Test\Modified_Solo Trumpet Performance by Aiman.mem"

#original_path = r"C:\Users\johnn\Desktop\DSP Project\New Test\C (flat 253Hz).mem"
#processed_path = r"C:\Users\johnn\Desktop\DSP Project\New Test\C (in-tune 261.63Hz).mem"

original_path = r"C:\Users\johnn\Desktop\DSP Project\New Test\Test Complete\Miniature Etude no4\Miniature Etude no 4.mem"
processed_path = r"C:\Users\johnn\Desktop\DSP Project\New Test\processed_output.mem"

# === Function to interpret unsigned binary as signed int16 ===
def bin_to_int16(b):
    val = int(b, 2)
    if val >= 2**15:
        val -= 2**16
    return np.int16(val)

# === Load .mem file safely ===
def load_mem(path):
    samples = []
    skipped = 0
    with open(path, "r") as f:
        lines = f.read().splitlines()
        for line in lines:
            line = line.strip()
            if not line:
                continue
            try:
                if set(line) <= {'0', '1'} and len(line) == 16:
                    val = bin_to_int16(line)
                else:
                    val = np.int16(int(line))
                samples.append(val)
            except Exception:
                skipped += 1
    print(f"✅ Loaded {len(samples)} samples from {os.path.basename(path)} (Skipped {skipped} invalid lines)")
    return np.array(samples, dtype=np.int16)

# === Load both files ===
original = load_mem(original_path)
processed = load_mem(processed_path)

# === Match length ===
min_len = min(len(original), len(processed))
original = original[:min_len]
processed = processed[:min_len]

# === Plot side-by-side ===
plt.figure(figsize=(14, 6))

plt.subplot(1, 2, 1)
plt.plot(original, color='steelblue')
plt.title("Original Waveform")
plt.xlabel("Sample Index")
plt.ylabel("Amplitude")
plt.grid(True)

plt.subplot(1, 2, 2)
plt.plot(processed, color='darkorange')
plt.title("Modified Waveform")
plt.xlabel("Sample Index")
plt.ylabel("Amplitude")
plt.grid(True)

plt.tight_layout()
plt.show()
