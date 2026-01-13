import tkinter as tk
from tkinter import ttk, messagebox
from main import TTSMic
from faster_whisper import WhisperModel

from pydub import AudioSegment
from pydub.playback import play
import sounddevice as sd
import soundfile as sf
import os
import threading
import numpy as np

fs = 44100
channels = 1

model_size = "small"

model = WhisperModel(model_size, device="cpu", compute_type="int8")
recording = False
text : str = None

def button_click():
    text = entry_box.get()

    if not text.strip():
        messagebox.showwarning("Warning", "Please enter some text!")
        return

    tts_mic = TTSMic()

    audio = tts_mic.generate_audio(
        text,
        float(speed_spinbox.get()),
        language_box.get(),
        float(pitch_spinbox.get())
    )

    tts_mic.play_to_both(audio)


def play_sound(path):
    audio = AudioSegment.from_file(path)
    play(audio)

def record_audio():
    global recording, text, stream, file
    print("running")
    if recording:
        recording = False
        entry_box.delete(0, tk.END)
        entry_box.insert(0, "Wait a moment...")

        stream.stop()
        stream.close()
        file.close()

        segments, info = model.transcribe("input.wav", beam_size=5)
        text = "".join(s.text for s in segments)

        entry_box.delete(0, tk.END)
        entry_box.insert(0, text)
        button_click()

        silent_data = np.zeros((int(fs * 5), channels), dtype=np.float32)
        sf.write("input.wav", silent_data, samplerate=fs)
    else:
        sound_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "new-notification-010-352755.mp3")
        threading.Thread(target=play_sound, args=(sound_path,), daemon=True).start()
        recording = True     
        entry_box.delete(0, tk.END)
        entry_box.insert(0, "Recording...")

        file = sf.SoundFile(
            "input.wav",
            mode="w",
            samplerate=fs,
            channels=channels,
            subtype="FLOAT"
        )

        def callback(indata, frames, time, status):
            file.write(indata)

        stream = sd.InputStream(
            samplerate=fs,
            channels=channels,
            callback=callback
        )

        stream.start()

root = tk.Tk()
root.title("TTS Microphone")
root.geometry("500x500")

# Text input
tk.Label(root, text="Enter text:").pack(pady=10)
entry_box = tk.Entry(root, width=60)
entry_box.pack(pady=5)

# Speed control
tk.Label(root, text="Speed:").pack(pady=2)

speed_var = tk.DoubleVar(value=1.0)
speed_spinbox = tk.Spinbox(
    root,
    from_=0.1,
    to=3.0,
    increment=0.1,
    textvariable=speed_var
)
speed_spinbox.pack(pady=10)


# Pitch control
tk.Label(root, text="Pitch:").pack(pady=2)

pitch_var = tk.IntVar(value=0)
pitch_spinbox = tk.Spinbox(
    root,
    from_=-100,
    to=100,
    increment=1,
    textvariable=pitch_var
)
pitch_spinbox.pack(pady=10)

# Language dropdown
tk.Label(root, text="Language:").pack(pady=2)

options = (
    "af", "sq", "am", "ar", "hy", "az", "bn", "bs", "bg", "ca", "zh-CN", "zh-TW",
    "hr", "cs", "da", "nl", "en", "en-au", "en-uk", "en-us", "eo", "et", "tl", "fi",
    "fr", "fr-ca", "gl", "ka", "de", "el", "gu", "ht", "he", "hi", "hu", "is", "id",
    "ga", "it", "ja", "jw", "kn", "kk", "km", "ko", "ku", "ky", "lo", "la", "lv",
    "lt", "mk", "mg", "ms", "ml", "mt", "mr", "mn", "my", "ne", "no", "ny", "ps", "fa",
    "pl", "pt", "pt-br", "pa", "ro", "ru", "sm", "gd", "sr", "st", "sn", "sd", "si",
    "sk", "sl", "so", "es", "es-us", "su", "sw", "sv", "tg", "ta", "te", "th", "tr", "uk"
)

language_box = ttk.Combobox(root, values=options, state="readonly")
language_box.set("en")
language_box.pack(pady=10)

# Submit
tk.Button(root, text="Record", command=record_audio).pack(pady=10)
root.bind("<F6>", lambda e: record_audio())
tk.Button(root, text="Enter", command=button_click).pack(pady=10)
root.bind("<Return>", lambda e: button_click())

root.mainloop()
