import numpy as np
import sounddevice as sd
import time
import librosa

SAMPLE_RATE = 44100
DURATION = 0.1  # seconds per recording
# DURATION = 1.0  # seconds per recording

def record_audio(duration, sample_rate):
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='float32')
    sd.wait()
    return recording.flatten()

def get_fundamental_freq(signal, sample_rate):
    try:
        f0 = librosa.yin(signal, fmin=100, fmax=1500, sr=sample_rate)
        return np.nanmean(f0)
    except Exception as e:
        print(f"Pitch detection error: {e}")
        return 0.0

def freq_to_note_name(freq):
    if freq <= 0 or np.isnan(freq):
        return "N/A"
    midi = librosa.hz_to_midi(freq)
    return librosa.midi_to_note(midi, octave=True, unicode=False)

def freq_to_trumpet_note(freq):
    if freq <= 0 or np.isnan(freq):
        return "N/A"
    midi = librosa.hz_to_midi(freq)
    transposed_midi = midi + 2
    return librosa.midi_to_note(transposed_midi, octave=True, unicode=False)

def start_recording(send_func=None, should_continue=lambda: True):
    timestamps, freqs, concert_notes, trumpet_notes = [], [], [], []
    start_time = time.time()

    print("🎙️ Recording...")

    while should_continue():
        now = time.time()
        elapsed = int(now - start_time)
        audio = record_audio(DURATION, SAMPLE_RATE)
        freq = get_fundamental_freq(audio, SAMPLE_RATE)
        concert = freq_to_note_name(freq)
        trumpet = freq_to_trumpet_note(freq)
        print(f"[{elapsed}s] {freq:.8f} Hz → Concert: {concert}, Trumpet: {trumpet}")

        if send_func:
            send_func(freq, concert, trumpet)

        timestamps.append(elapsed)
        freqs.append(freq)
        concert_notes.append(concert)
        trumpet_notes.append(trumpet)

        time.sleep(0.1)

    print("🛑 Recording ended.")
    return timestamps, freqs, concert_notes, trumpet_notes
