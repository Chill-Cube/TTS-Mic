import tkinter as tk
from tkinter import ttk, messagebox
from main import TTSMic


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


root = tk.Tk()
root.title("TTS Microphone")
root.geometry("500x300")

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
tk.Button(root, text="Enter", command=button_click).pack(pady=10)
root.bind("<Return>", lambda e: button_click())

root.mainloop()
