import io
from gtts import gTTS
from pydub import AudioSegment
from pydub.utils import which
import threading

AudioSegment.converter = which("ffmpeg")


import sounddevice as sd
import numpy as np

class TTSMic:
    def __init__(self, virtual_device_name="CABLE Input"):
        self.virtual_device_name = virtual_device_name

    def generate_audio(self, text: str, lang='en', speed=False) -> AudioSegment:
        tts = gTTS(text=text, lang=lang, slow=speed)
        mp3_fp = io.BytesIO()
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)
        audio = AudioSegment.from_file(mp3_fp, format="mp3")
        return audio

    def play_audio(self, audio: AudioSegment, device_name=None):
        import sounddevice as sd
        import numpy as np

        samples = np.array(audio.get_array_of_samples())
        if audio.channels == 2:
            samples = samples.reshape((-1, 2))
        samples = samples.astype(np.float32) / (2 ** 15)

        device_id = None
        if device_name:
            devices = sd.query_devices()
            for i, dev in enumerate(devices):
                if device_name.lower() in dev['name'].lower():
                    device_id = i
                    break
        sd.play(samples, samplerate=audio.frame_rate, device=device_id)
        sd.wait()

    def play_to_virtual(self, audio: AudioSegment):
        self.play_audio(audio, self.virtual_device_name)

    def play_to_speakers(self, audio: AudioSegment):
        self.play_audio(audio, device_name="Realtek(R) Audio")

    def play_to_both(self, audio: AudioSegment):
        threading.Thread(target=self.play_to_virtual, args=(audio,), daemon=True).start()
        threading.Thread(target=self.play_to_speakers, args=(audio,), daemon=True).start()
