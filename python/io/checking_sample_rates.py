import scipy.io.wavfile as wav

# Load both files
rate_orig, data_orig = wav.read(r"C:\Users\johnn\Desktop\DSP Project\New Test\Inputs\Solo Trumpet Performance by Aiman.wav")
rate_proc, data_proc = wav.read(r"C:\Users\johnn\Desktop\DSP Project\New Test\Modified_Solo Trumpet Performance by Aiman.wav")

print(f"Original sample rate: {rate_orig}, duration: {len(data_orig)/rate_orig:.2f} sec")
print(f"Processed sample rate: {rate_proc}, duration: {len(data_proc)/rate_proc:.2f} sec")
