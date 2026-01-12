import io
from gtts import gTTS
from pydub import AudioSegment
from pydub.utils import which
import librosa
import threading

AudioSegment.converter = which("ffmpeg")


import sounddevice as sd
import numpy as np


def change_speed(audio: AudioSegment, speed: float) -> AudioSegment:
    speed = float(speed)

    if speed == 1.0:
        return audio

    if speed > 1.0:
        return audio.speedup(playback_speed=speed)

     # Slow down
    new_rate = int(audio.frame_rate * speed)
    return audio._spawn(
        audio.raw_data,
        overrides={"frame_rate": new_rate}
    ).set_frame_rate(audio.frame_rate)

def change_pitch(audio: AudioSegment, semitones: float) -> AudioSegment:
    samples = np.array(audio.get_array_of_samples()).astype(np.float32)
    samples /= np.iinfo(audio.array_type).max

    y = librosa.effects.pitch_shift(
        samples,
        sr=audio.frame_rate,
        n_steps=semitones
    )

    y = (y * np.iinfo(audio.array_type).max).astype(audio.array_type)

    return audio._spawn(y.tobytes())

class TTSMic:
    def __init__(self, virtual_device_name="CABLE Input"):
        self.virtual_device_name = virtual_device_name

    def generate_audio(self, text: str, speed, lang:str, pitch) -> AudioSegment:
        tts = gTTS(text=text, lang=lang, slow=False)
        mp3_fp = io.BytesIO()
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)
        audio = AudioSegment.from_file(mp3_fp, format="mp3")


        print(type(speed))
        audio = change_speed(audio, speed)
        audio = change_pitch(audio, pitch)

        return audio

    def play_audio(self, audio: AudioSegment, device_name=None):
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
        default_output = sd.default.device[1]
        device_info = sd.query_devices(default_output)
        self.play_audio(audio, device_name=device_info['name'])

    def play_to_both(self, audio: AudioSegment):
        threading.Thread(target=self.play_to_virtual, args=(audio,), daemon=True).start()
        threading.Thread(target=self.play_to_speakers, args=(audio,), daemon=True).start()
