from scipy.io import wavfile

# Replace with path to your original WAV file
original_wav = r"C:\Users\johnn\Desktop\DSP Project\New Test\Test Complete\Miniature Etude no4\Miniature Etude no 4.wav"

# Read the WAV file
sample_rate, data = wavfile.read(original_wav)

print(f"🎧 Sample rate: {sample_rate} Hz")
print(f"📊 Number of samples: {len(data)}")
