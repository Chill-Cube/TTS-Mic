import tkinter as tk
from tkinter import messagebox
from tts import TTSMic


def button_click():
    # Retrieve text from entry box
    text = entry_box.get()
    
    if not text.strip():
        tk.messagebox.showwarning("Warning", "Please enter some text!")
        return

    # Generate and play audio
    tts_mic = TTSMic()    
    audio = tts_mic.generate_audio(text)
    tts_mic.play_to_both(audio)

root = tk.Tk()
root.title("TTS Microphone")
root.geometry("300x150")

label = tk.Label(root, text="Enter text:")
label.pack(pady=10)

entry_box = tk.Entry(root, width=60)
entry_box.pack(pady=5)

enter_button = tk.Button(root, text="Enter", command=button_click)
enter_button.pack(pady=10)

root.bind('<Return>', lambda event: button_click())
root.mainloop()