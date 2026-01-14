from pydub import AudioSegment
from pydub.playback import play
import sounddevice as sd
import soundfile as sf
import numpy as np
from faster_whisper import WhisperModel
import os
import threading

fs = 44100
channels = 1

model_size = "small"

model = WhisperModel(model_size, device="cpu", compute_type="int8")
currently_recording = False
text : str = None
stream = None
file = None

def play_sound(path):
    audio = AudioSegment.from_file(path)
    play(audio)

class VoiceRecord:
    def __init__(self):
        self.stream = None
        self.file = None
        self.recording = False

    def start_recording(self):
        if self.recording:
            return
        
        sound_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "new-notification-010-352755.mp3")
        threading.Thread(target=play_sound, args=(sound_path,), daemon=True).start()

        self.recording = True

        self.file = sf.SoundFile(
            "input.wav",
            mode="w",
            samplerate=fs,
            channels=channels,
            subtype="FLOAT"
        )

        def callback(indata, frames, time, status):
            if self.recording:
                self.file.write(indata)

        self.stream = sd.InputStream(
            samplerate=fs,
            channels=channels,
            callback=callback
        )
        self.stream.start()

    def stop_recording(self) -> str | None:
        if not self.recording:
            return None
        
        sound_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "done.mp3")
        threading.Thread(target=play_sound, args=(sound_path,), daemon=True).start()

        self.recording = False

        try:
            if self.stream:
                self.stream.stop()
                self.stream.close()
            if self.file:
                self.file.close()

            segments, _ = model.transcribe("input.wav", beam_size=5)
            return "".join(s.text for s in segments)

        finally:
            silent_data = np.zeros((int(fs * 5), channels), dtype=np.float32)
            sf.write("input.wav", silent_data, samplerate=fs)

            self.stream = None
            self.file = None

    def cancel_record(self):
        if not self.recording:
            return

        self.recording = False

        if self.stream:
            self.stream.stop()
            self.stream.close()
        if self.file:
            self.file.close()

        silent_data = np.zeros((int(fs * 5), channels), dtype=np.float32)
        sf.write("input.wav", silent_data, samplerate=fs)

        self.stream = None
        self.file = None
