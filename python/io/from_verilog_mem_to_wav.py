import numpy as np
from scipy.io.wavfile import write
import os
import re
import shutil  # <-- Import for copying files

# === ONLY CHANGE THESE ===
mem_path = r"C:\Users\johnn\Desktop\DSP Project\New Test\project_1\project_1.sim\sim_1\behav\xsim\processed_output.mem"
output_folder = r"C:\Users\johnn\Desktop\DSP Project\New Test"

# === Auto-detect sample rate from filename ===
match = re.search(r"(\d{4,6})", mem_path)
sample_rate = int(match.group(1)) if match else 44100

# === Create output folder if it doesn't exist ===
os.makedirs(output_folder, exist_ok=True)

# === Build output .wav file path ===
base_filename = os.path.splitext(os.path.basename(mem_path))[0]
output_wav = os.path.join(output_folder, base_filename + ".wav")

# === Read and clean .mem lines ===
with open(mem_path, "r") as f:
    lines = f.read().splitlines()

samples = []
skipped = 0

for line in lines:
    line = line.strip()
    if line.lstrip("-").isdigit():
        samples.append(np.int16(line))
    else:
        skipped += 1

samples = np.array(samples, dtype=np.int16)

# === Write the WAV file ===
write(output_wav, sample_rate, samples)

# === Copy .mem file to output folder ===
destination_mem = os.path.join(output_folder, os.path.basename(mem_path))
shutil.copy2(mem_path, destination_mem)

# === Done! ===
print(f"✅ Converted {mem_path} → {output_wav}")
print(f"   📦 {len(samples)} samples written at {sample_rate} Hz")
if skipped > 0:
    print(f"   ⚠️  Skipped {skipped} invalid lines (e.g., 'x', 'z', or empty')")
print(f"📁 Copied original .mem to: {destination_mem}")
