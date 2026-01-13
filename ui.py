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
currently_recording = False
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
    global recording, text, stream, file, currently_recording
    print("running")

    if currently_recording:
        return
    
    if recording:
        recording = False
        currently_recording = False
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
        currently_recording = False 
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

def cancel_record():
    global recording, currently_recording, stream, file
    if recording:
        recording = False
        currently_recording = False
        if stream:
            stream.stop()
            stream.close()
        if file:
            file.close()
        entry_box.delete(0, tk.END)

        silent_data = np.zeros((int(fs * 5), channels), dtype=np.float32)
        sf.write("input.wav", silent_data, samplerate=fs)

root = tk.Tk()
root.title("TTS Microphone")
root.geometry("500x250")
root.resizable(False, False)

main_frame = tk.Frame(root, padx=20, pady=20)
main_frame.pack(expand=True)

# Speed and Pitch variables
speed_var = tk.DoubleVar(value=1.0)
pitch_var = tk.IntVar(value=0)

# Language options
options = (
    "af", "sq", "am", "ar", "hy", "az", "bn", "bs", "bg", "ca", "zh-CN", "zh-TW",
    "hr", "cs", "da", "nl", "en", "en-au", "en-uk", "en-us", "eo", "et", "tl", "fi",
    "fr", "fr-ca", "gl", "ka", "de", "el", "gu", "ht", "he", "hi", "hu", "is", "id",
    "ga", "it", "ja", "jw", "kn", "kk", "km", "ko", "ku", "ky", "lo", "la", "lv",
    "lt", "mk", "mg", "ms", "ml", "mt", "mr", "mn", "my", "ne", "no", "ny", "ps", "fa",
    "pl", "pt", "pt-br", "pa", "ro", "ru", "sm", "gd", "sr", "st", "sn", "sd", "si",
    "sk", "sl", "so", "es", "es-us", "su", "sw", "sv", "tg", "ta", "te", "th", "tr", "uk"
)

# Main frame
main_frame = tk.Frame(root, padx=20, pady=20)
main_frame.pack(fill="both", expand=True)

# Text input
tk.Label(main_frame, text="Enter text:", font=("Helvetica", 12)).pack(pady=(0,5))
entry_box = tk.Entry(main_frame, width=45, font=("Helvetica", 12))
entry_box.pack(pady=(0,15))

# Speed and Pitch frame
sp_frame = tk.Frame(main_frame)
sp_frame.pack(pady=(0,15))

tk.Label(sp_frame, text="Speed:", font=("Helvetica", 10)).grid(row=0, column=0, padx=5)
speed_spinbox = tk.Spinbox(sp_frame, from_=0.1, to=3.0, increment=0.1, width=5, textvariable=speed_var)
speed_spinbox.grid(row=0, column=1, padx=5)

tk.Label(sp_frame, text="Pitch:", font=("Helvetica", 10)).grid(row=0, column=2, padx=5)
pitch_spinbox = tk.Spinbox(sp_frame, from_=-100, to=100, increment=1, width=5, textvariable=pitch_var)
pitch_spinbox.grid(row=0, column=3, padx=5)

# Language selection
tk.Label(main_frame, text="Language:", font=("Helvetica", 12)).pack(pady=(0,5))
language_box = ttk.Combobox(main_frame, values=options, state="readonly", width=20, font=("Helvetica", 10))
language_box.set("en")
language_box.pack(pady=(0,15))

# Buttons frame
btn_frame = tk.Frame(main_frame)
btn_frame.pack(pady=(10,0))

record_btn = tk.Button(btn_frame, text="Record", width=12, command=record_audio)
record_btn.grid(row=0, column=0, padx=5)

cancel_btn = tk.Button(btn_frame, text="Cancel Record", width=12, command=cancel_record)
cancel_btn.grid(row=0, column=1, padx=5)

enter_btn = tk.Button(btn_frame, text="Enter", width=12, command=button_click)
enter_btn.grid(row=0, column=2, padx=5)

# Key bindings
root.bind("<F6>", lambda e: record_audio())
root.bind("<F7>", lambda e: cancel_record())
root.bind("<Return>", lambda e: button_click())

root.mainloop()
