import tkinter as tk
from tkinter import ttk, messagebox
from tts import TTSMic
from voice import VoiceRecord

recorder = VoiceRecord()

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


def record_audio():
    if recorder.recording:
        
        entry_box.delete(0, tk.END)
        entry_box.insert(0, "Processing...")
        entry_box.update()
        text = recorder.stop_recording()
        record_btn.config(text="Record")

        if text:
            entry_box.delete(0, tk.END)
            entry_box.insert(0, text)

        button_click()
    else:
        recorder.start_recording()
        record_btn.config(text="Stop Record")
        entry_box.delete(0, tk.END)
        entry_box.insert(0, "Recording...")
        entry_box.update()


def cancel_record():
    recorder.cancel_record()
    record_btn.config(text="Record")
    entry_box.delete(0, tk.END)


root = tk.Tk()
root.title("TTS Microphone")
root.geometry("500x250")
root.resizable(False, False)

main_frame = tk.Frame(root, padx=20, pady=20)
main_frame.pack(fill="both", expand=True)

speed_var = tk.DoubleVar(value=1.0)
pitch_var = tk.IntVar(value=0)

options = (
    "af","sq","am","ar","hy","az","bn","bs","bg","ca","zh-CN","zh-TW","hr","cs","da",
    "nl","en","en-au","en-uk","en-us","eo","et","tl","fi","fr","fr-ca","gl","ka","de",
    "el","gu","ht","he","hi","hu","is","id","ga","it","ja","jw","kn","kk","km","ko",
    "ku","ky","lo","la","lv","lt","mk","mg","ms","ml","mt","mr","mn","my","ne","no",
    "ny","ps","fa","pl","pt","pt-br","pa","ro","ru","sm","gd","sr","st","sn","sd",
    "si","sk","sl","so","es","es-us","su","sw","sv","tg","ta","te","th","tr","uk"
)

tk.Label(main_frame, text="Enter text:", font=("Helvetica", 12)).pack(pady=(0, 5))
entry_box = tk.Entry(main_frame, width=45, font=("Helvetica", 12))
entry_box.pack(pady=(0, 15))

sp_frame = tk.Frame(main_frame)
sp_frame.pack(pady=(0, 15))

tk.Label(sp_frame, text="Speed:").grid(row=0, column=0, padx=5)
speed_spinbox = tk.Spinbox(
    sp_frame, from_=0.1, to=3.0, increment=0.1, width=5, textvariable=speed_var
)
speed_spinbox.grid(row=0, column=1, padx=5)

tk.Label(sp_frame, text="Pitch:").grid(row=0, column=2, padx=5)
pitch_spinbox = tk.Spinbox(
    sp_frame, from_=-100, to=100, increment=1, width=5, textvariable=pitch_var
)
pitch_spinbox.grid(row=0, column=3, padx=5)

tk.Label(main_frame, text="Language:", font=("Helvetica", 12)).pack(pady=(0, 5))
language_box = ttk.Combobox(
    main_frame, values=options, state="readonly", width=20
)
language_box.set("en")
language_box.pack(pady=(0, 15))

btn_frame = tk.Frame(main_frame)
btn_frame.pack(pady=(10, 0))

record_btn = tk.Button(btn_frame, text="Record", width=12, command=record_audio)
record_btn.grid(row=0, column=0, padx=5)

cancel_btn = tk.Button(btn_frame, text="Cancel Record", width=12, command=cancel_record)
cancel_btn.grid(row=0, column=1, padx=5)

enter_btn = tk.Button(btn_frame, text="Enter", width=12, command=button_click)
enter_btn.grid(row=0, column=2, padx=5)

root.bind("<F6>", lambda e: record_audio())
root.bind("<F7>", lambda e: cancel_record())
root.bind("<Return>", lambda e: button_click())

root.mainloop()
