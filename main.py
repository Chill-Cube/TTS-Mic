import pyaudio
from gtts import gTTS
import os

import subprocess
import sys

class VB_Cable:
    def __init__(self):
        subprocess.run(
            ["VBCABLE_Setup_x64.exe", "-i", "-h"],
            check=True
        )

class TTS:
    def __init__(self):
        self.p = pyaudio.PyAudio()

    def generate(self, text: str, lang: str = 'en', speed: bool = False) -> bytes:
        tts = gTTS(text=text, lang=lang, slow=speed)
        temp_file = "temp_audio.mp3"
        tts.save(temp_file)
        
        with open(temp_file, "rb") as f:
            audio_data = f.read()
        
        os.remove(temp_file)
        return audio_data
    
    def play_audio(self, audio_data: bytes):
        pass