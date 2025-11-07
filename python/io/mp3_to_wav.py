#!/usr/bin/env python3
from pydub import AudioSegment

def convert_mp3_to_wav():
    # Hard-coded input and output paths **including filename**
    input_mp3  = r"C:\Users\johnn\Downloads\Miniature Etude no 4.mp3"
    output_wav = r"C:\Users\johnn\Desktop\DSP Project\New Test\Miniature Etude no 4.wav"
    
    # Load the MP3 and export as WAV
    audio = AudioSegment.from_mp3(input_mp3)
    audio.export(output_wav, format="wav")
    
    print(f"Successfully converted '{input_mp3}' → '{output_wav}'")

if __name__ == "__main__":
    convert_mp3_to_wav()
